# src/registration/services.py
import logging
import os
import secrets
from io import BytesIO
from datetime import datetime, timezone, timedelta
import uuid
import re # Importar para validación de regex de contraseña

import aiofiles
from fastapi import UploadFile, HTTPException, status # Importar HTTPException y status
from PIL import Image
from sqlalchemy import or_, update
from sqlalchemy.future import select as sa_select # Renombrado para evitar conflicto con la función de Python `select`
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload

from app.config import settings
from app.models import Usuario
from app.registration.schemas import UsuarioRegisterSchema
from app.authentication.models import EmailConfirmationToken
from app.email.email_service import email_service
from app.utils import get_hashed_password
from app.services.cloud_storage import upload_to_r2

logger = logging.getLogger(__name__)

DEFAULT_CHUNK_SIZE = 1024 * 1024 * 1  # 1 megabyte

TEST_EMAILS_BYPASS = {
    "test_user_1784867943983167886@testuser.com",
    "test_user01@gmail.com",
    "test_user02@gmail.com",
    "Benjamin@oppychat.com"
    # Agrega otros correos de prueba de MP si es necesario para otros países:
    # "test_user_OTRO_PAIS@testuser.com",
}

TEST_EMAIL_REDIRECT = None

# --- Función para validar la complejidad de la contraseña (se mantiene sin cambios) ---
def validate_password_complexity(password: str):
    """
    Valida la complejidad de la contraseña.
    Requiere:
    - Mínimo 8 caracteres
    - Al menos una letra mayúscula
    - Al menos una letra minúscula
    - Al menos un número
    - Al menos un carácter especial (ej. !@#$%^&*)
    """
    if len(password) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La contraseña debe tener al menos 8 caracteres."
        )
    if not re.search(r"[A-Z]", password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La contraseña debe contener al menos una letra mayúscula."
        )
    if not re.search(r"[a-z]", password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La contraseña debe contener al menos una letra minúscula."
        )
    if not re.search(r"\d", password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La contraseña debe contener al menos un número."
        )
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La contraseña debe contener al menos un carácter especial."
        )
    if ' ' in password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La contraseña no puede contener espacios."
        )

# --- Se corrige la función 'select' de sqlalchemy para evitar conflicto con 'select' de Python ---
async def get_user_by_email_or_username(db_session: AsyncSession, *, email: str, username: str) -> Usuario | None:
    """
    Obtiene un usuario por su email o nombre de usuario.
    """
    query = sa_select(Usuario).where(or_(Usuario.email == email, Usuario.username == username))
    result = await db_session.execute(query)
    user: Usuario | None = result.scalar_one_or_none()
    return user

async def create_user_from_confirmation(
    db_session: AsyncSession,
    *,
    user_data: dict,
) -> Usuario:
    """
    Crea un nuevo usuario en la base de datos a partir de los datos de un token
    de confirmación. Asume que la validación de email/username ya se hizo.
    """
    try:
        new_user = Usuario(
            username=user_data["username"].lower(),
            email=user_data["email"].lower(),
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
            hashed_password=user_data["password_hash"],
            has_accepted_terms=user_data["terms_accepted"],
            user_image=user_data["image_url"], # Usa la URL de la imagen del token
            is_deleted=False,
        )

        referral_code = user_data.get("referral_code")
        if referral_code:
            # Encuentra al usuario que invitó
            referrer_query = sa_select(Usuario).where(Usuario.username == referral_code.lower())
            referrer_result = await db_session.execute(referrer_query)
            referrer = referrer_result.scalar_one_or_none()
            
            if referrer:
                new_user.referred_by_id = referrer.id
                
                # Otorga créditos y nivel al referidor si no ha llegado al tope
                if referrer.bonus_credits_balance < 250:
                    referrer.bonus_credits_balance += 50
                    if referrer.bonus_credits_balance > 250:
                        referrer.bonus_credits_balance = 250
                    
                    # Ascender a EMBAJADOR si no lo es y si tiene un plan menor
                    if referrer.freemium_tier == "PREMIUM":
                        referrer.freemium_tier = "AMBASSADOR"
                
                # Aumenta el contador de notificaciones no leídas
                referrer.unread_referrals_count += 1
                db_session.add(referrer)

        db_session.add(new_user)
        await db_session.commit()
        await db_session.refresh(new_user)
        
    except IntegrityError as e:
        await db_session.rollback()
        if "users_email_key" in str(e) or "email" in str(e).lower():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Ya existe un usuario con este correo electrónico."
            )
        else:
            logger.error(f"Error de integridad al crear usuario: {e}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Ocurrió un error inesperado."
            )
    except Exception as e:
        await db_session.rollback()
        logger.error(f"Error inesperado y no manejado al crear usuario {user_data.get('username')}: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocurrió un error inesperado al registrar el usuario."
        )

    return new_user

# --- FUNCIONES PARA EL FLUJO DE CONFIRMACIÓN DE EMAIL ---

async def register_user_and_send_confirmation(
    db_session: AsyncSession,
    user_schema: UsuarioRegisterSchema,
    uploaded_image: UploadFile | None = None
):
    """
    Gestiona el flujo de registro. Si el email es un email de prueba conocido,
    se salta la confirmación y crea el usuario inmediatamente.
    """
    
    # 1. Validar si el email de prueba requiere bypass
    user_email_lower = user_schema.email.lower()
    
    hashed_password = await get_hashed_password(user_schema.password)
    
    image_url = None
    if uploaded_image:
        # Asumo que ImageSaver es una clase existente en tu codebase
        image_saver = ImageSaver(db_session=db_session)
        image_url = await image_saver.save_user_image(uploaded_image, user_schema.username)

    # 2. Invalida tokens previos no usados para este email (importante antes de cualquier acción)
    await db_session.execute(
        update(EmailConfirmationToken)
        .where(
            EmailConfirmationToken.user_email == user_email_lower,
            EmailConfirmationToken.is_used == False,
        )
        .values(is_used=True)
    )
    await db_session.commit()

    # 3. Validar si el correo está en bypass (pruebas o demos)
    is_bypass = (user_email_lower in TEST_EMAILS_BYPASS) or user_email_lower.endswith(('@oppytest.com', '@demo.oppytalent.com'))

    # 4. Guardar los datos del usuario en la tabla de tokens (necesario incluso para el bypass)
    confirmation_token_entry = EmailConfirmationToken(
        user_email=user_email_lower,
        token=secrets.token_urlsafe(32),
        username=user_schema.username.lower(),
        password_hash=hashed_password,
        first_name=user_schema.first_name,
        last_name=user_schema.last_name,
        terms_accepted=user_schema.terms_accepted,
        image_url=image_url,
        referral_code=user_schema.referral_code,
        expires_at=datetime.now(timezone.utc) + timedelta(minutes=60),
        is_used=is_bypass # Marcar como usado si es bypass
    )
    db_session.add(confirmation_token_entry)
    await db_session.commit()
    await db_session.refresh(confirmation_token_entry)

    # ⭐️ LÓGICA DE BYPASS (Exención para testing y cuentas demo) ⭐️
    if is_bypass:
        logger.info(f"Bypassing email confirmation for test/demo user: {user_email_lower}")
        
        user_data = {
            "username": confirmation_token_entry.username,
            "email": confirmation_token_entry.user_email,
            "first_name": confirmation_token_entry.first_name,
            "last_name": confirmation_token_entry.last_name,
            "password_hash": confirmation_token_entry.password_hash,
            "terms_accepted": confirmation_token_entry.terms_accepted,
            "image_url": confirmation_token_entry.image_url,
            "referral_code": confirmation_token_entry.referral_code,
        }
        await create_user_from_confirmation(db_session, user_data=user_data)

        return {"message": "Usuario creado exitosamente (Confirmación de email omitida).", "user_created": True, "email": user_schema.email}
    
    # ⭐️ FLUJO NORMAL (Enviar Email) ⭐️
    base = str(settings.API_URL).rstrip('/')
    if not base.endswith('/api'):
        base += '/api'

    # Ruta exacta del router en el backend montado en /api/v1/auth
    confirmation_url = f"{base}/v1/auth/confirm-email/{confirmation_token_entry.token}"

    context = {
        "user_name": user_schema.first_name or user_schema.username or user_schema.email,
        "confirmation_url": confirmation_url,
        "app_name": "OppyTalent",
        "expiration_minutes": 60,
    }
    
    subject = "Activa tu Agente de IA en OppyTalent"

    if TEST_EMAIL_REDIRECT:
        recipients_list = [TEST_EMAIL_REDIRECT]
        logger.warning(f"DEBUG: Email de confirmación para '{user_schema.email}' redirigido a: {TEST_EMAIL_REDIRECT}")
        subject = f"[REDIRECTED - ORIGINAL: {user_schema.email}] {subject}"
    else:
        recipients_list = [user_schema.email]
        
    await email_service.send_email(
        subject=subject,
        recipients=recipients_list,
        template_name="email_confirmation.html",
        template_vars=context,
    )

    return {"message": "Email de confirmación enviado exitosamente.", "user_created": False, "email": user_schema.email}


async def confirm_user_email(db_session: AsyncSession, token: str) -> dict:
    result = await db_session.execute(
        sa_select(EmailConfirmationToken).where(EmailConfirmationToken.token == token)
    )
    token_entry = result.scalar_one_or_none()

    if (
        not token_entry
        or token_entry.is_used
        or (
            token_entry.expires_at and
            (
                (token_entry.expires_at.tzinfo is None and token_entry.expires_at.replace(tzinfo=timezone.utc) < datetime.now(timezone.utc))
                or (token_entry.expires_at.tzinfo is not None and token_entry.expires_at < datetime.now(timezone.utc))
            )
        )
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El enlace de confirmación es inválido o ha expirado."
        )

    token_entry.is_used = True
    await db_session.commit()

    user_data = {
        "username": token_entry.username,
        "email": token_entry.user_email,
        "first_name": token_entry.first_name,
        "last_name": token_entry.last_name,
        "password_hash": token_entry.password_hash,
        "terms_accepted": token_entry.terms_accepted,
        "image_url": token_entry.image_url,
        "referral_code": token_entry.referral_code,
    }

    await create_user_from_confirmation(db_session, user_data=user_data)

    await db_session.delete(token_entry)
    await db_session.commit()

    return {"message": "Correo electrónico confirmado. Usuario creado exitosamente."}

# --- CLASE ImageSaver UNIFICADA Y CORREGIDA ---
class ImageSaver:
    def __init__(self, db_session: AsyncSession):
        self.db_session: AsyncSession = db_session

    async def save_user_image(self, uploaded_image: UploadFile, username: str) -> str | None:
        """
        Guarda la imagen de perfil usando Cloudflare R2 exclusivamente.
        """
        try:
            content = await uploaded_image.read()
            file_extension = uploaded_image.filename.split(".")[-1].lower() if uploaded_image.filename else "webp"
            filename = f"profile_{username}.{file_extension}"
            
            # Subir directamente a R2
            url = await upload_to_r2(content, filename, uploaded_image.content_type)
            return url
        except Exception as e:
            logger.error(f"Error al guardar la imagen para el usuario {username}: {e}", exc_info=True)
            return None
