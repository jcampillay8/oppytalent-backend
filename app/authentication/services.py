from uuid import UUID
# src/authentication/services.py
import asyncio
import secrets
import string
import logging
from datetime import datetime, timedelta, timezone

from fastapi import Request, BackgroundTasks
from sqlalchemy import and_, or_, select, update, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models import Usuario
from app.authentication.models import UsuarioSessionHistory, PasswordResetToken, RefreshToken
from app.config import settings
from app.utils import get_hashed_password, verify_password, needs_rehash
from app.email.email_service import email_service

logger = logging.getLogger(__name__)

# --- BÚSQUEDA DE USUARIOS ---

async def get_user_by_login_identifier(db_session: AsyncSession, *, login_identifier: str) -> Usuario | None:
    """Busca un usuario por email o username de forma eficiente."""
    query = (
        select(Usuario)
        .where(
            or_(Usuario.email == login_identifier, Usuario.username == login_identifier)
        )
    )
    result = await db_session.execute(query)
    return result.scalar_one_or_none()

async def get_user_by_email(db_session: AsyncSession, *, email: str) -> Usuario | None:
    """Busca específicamente por email."""
    query = (
        select(Usuario)
        .where(Usuario.email == email)
    )
    result = await db_session.execute(query)
    return result.scalar_one_or_none()

# --- AUTENTICACIÓN Y SESIONES ---
async def authenticate_user(db_session: AsyncSession, login_identifier: str, password: str, request: Request | None = None, allow_multiple: bool = False) -> Usuario | None:
    """Valida credenciales de forma simple."""
    user = await get_user_by_login_identifier(db_session, login_identifier=login_identifier)
    
    if not user:
        return None

    is_valid = await verify_password(password, user.hashed_password)
    if not is_valid:
        return None

    # Migración en caliente a Argon2
    if await needs_rehash(user.hashed_password):
        user.hashed_password = await get_hashed_password(password)

    if request:
        await create_user_session_history(db_session, user.id, request)

    await db_session.flush()
    return user

async def create_user_session_history(db_session: AsyncSession, user_id: UUID, request: Request) -> None:
    """Registra los metadatos de la sesión actual."""
    session_entry = UsuarioSessionHistory(
        user_id=user_id,
        login_time=datetime.now(timezone.utc),
        ip_address=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent")
    )
    db_session.add(session_entry)

async def update_user_session_logout_time(db_session: AsyncSession, user_id: UUID, request: Request) -> None:
    """Marca el fin de la sesión para una IP específica."""
    ip_address = request.client.host if request.client else None
    stmt = (
        update(UsuarioSessionHistory)
        .where(
            and_(
                UsuarioSessionHistory.user_id == user_id,
                UsuarioSessionHistory.logout_time.is_(None),
                UsuarioSessionHistory.ip_address == ip_address
            )
        )
        .values(logout_time=datetime.now(timezone.utc))
    )
    await db_session.execute(stmt)
    await db_session.commit()

# --- GOOGLE OAUTH ---

async def create_user_from_google_credentials(
    db_session: AsyncSession,
    email: str,
    given_name: str = "",
    family_name: str = "",
    picture: str | None = None,
    request: Request | None = None
) -> Usuario:
    """Crea un usuario desde Google con contraseña aleatoria segura."""
    alphabet = string.ascii_letters + string.digits + string.punctuation
    random_pass = "".join(secrets.choice(alphabet) for _ in range(24))
    
    user = Usuario(
        username=email,
        email=email,
        hashed_password=await get_hashed_password(random_pass)
    )
    db_session.add(user)
    await db_session.flush() # Para obtener el ID antes del commit final

    if request:
        await create_user_session_history(db_session, user.id, request)
    
    await db_session.flush()
    await db_session.refresh(user)
    return user

# --- PASSWORD RESET ---

async def generate_password_reset_token(db_session: AsyncSession, user: Usuario) -> str:
    """Genera token y revoca los anteriores no usados."""
    await db_session.execute(
        update(PasswordResetToken)
        .where(and_(PasswordResetToken.user_id == user.id, PasswordResetToken.is_used.is_(False)))
        .values(is_used=True)
    )
    
    token = secrets.token_urlsafe(32)
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=settings.PASSWORD_RESET_TOKEN_EXPIRE_MINUTES)

    reset_entry = PasswordResetToken(
        user_id=user.id,
        token=token,
        expires_at=expires_at,
        is_used=False
    )
    db_session.add(reset_entry)
    await db_session.commit()
    return token

async def verify_password_reset_token(db_session: AsyncSession, token: str) -> Usuario:
    """Valida el token de forma robusta."""
    query = select(PasswordResetToken).where(PasswordResetToken.token == token)
    result = await db_session.execute(query)
    token_entry = result.scalar_one_or_none()

    if not token_entry:
        raise ValueError("Token inválido.")
    if token_entry.is_used:
        raise ValueError("Token ya utilizado.")
    
    # 🚀 Comparación directa de fechas con zona horaria
    if token_entry.expires_at < datetime.now(timezone.utc):
        raise ValueError("Token expirado.")

    user = await db_session.get(Usuario, token_entry.user_id)
    if not user or user.is_deleted:
        raise ValueError("Usuario no disponible.")
        
    return user

async def reset_user_password(db_session: AsyncSession, user_id: UUID, token: str, new_password: str) -> None:
    """Actualiza la contraseña y quema el token."""
    user = await db_session.get(Usuario, user_id)
    if not user:
        raise ValueError("Usuario no encontrado.")

    user.hashed_password = await get_hashed_password(new_password)
    
    await db_session.execute(
        update(PasswordResetToken)
        .where(PasswordResetToken.token == token)
        .values(is_used=True)
    )
    await db_session.commit()

# --- REFRESH TOKENS ---

async def create_refresh_token_db_entry(
    db_session: AsyncSession,
    user_id: UUID,
    token: str,
    expires_at: datetime,
    request: Request
) -> None:
    """Registra el refresh token con info del dispositivo."""
    entry = RefreshToken(
        user_id=user_id,
        token=token,
        expires_at=expires_at,
        ip_address=request.client.host if request.client else None,
        user_agent=request.headers.get("user-agent")
    )
    db_session.add(entry)
    await db_session.commit()

async def revoke_refresh_token(db_session: AsyncSession, token: str) -> bool:
    """Revoca un token específico."""
    stmt = (
        update(RefreshToken)
        .where(and_(RefreshToken.token == token, RefreshToken.is_revoked.is_(False)))
        .values(is_revoked=True)
    )
    result = await db_session.execute(stmt)
    await db_session.commit()
    return result.rowcount > 0

async def revoke_all_user_sessions(db_session: AsyncSession, user_id: UUID) -> int:
    """Revoca todos los tokens activos (Cierre de sesión global)."""
    stmt = (
        update(RefreshToken)
        .where(and_(RefreshToken.user_id == user_id, RefreshToken.is_revoked.is_(False)))
        .values(is_revoked=True)
    )
    result = await db_session.execute(stmt)
    await db_session.commit()
    return result.rowcount

async def get_user_by_refresh_token(db_session: AsyncSession, token: str) -> Usuario | None:
    """
    Verifica si un refresh token existe, no está revocado y no ha expirado.
    Retorna al usuario asociado.
    """
    query = (
        select(RefreshToken)
        .where(
            and_(
                RefreshToken.token == token,
                RefreshToken.is_revoked.is_(False),
                RefreshToken.expires_at > datetime.now(timezone.utc)
            )
        )
    )
    result = await db_session.execute(query)
    token_entry = result.scalar_one_or_none()

    if not token_entry:
        return None

    return await db_session.get(Usuario, token_entry.user_id)

# --- ORQUESTADOR DE CONTRASEÑA OLVIDADA ---

async def process_forgot_password(
    db_session: AsyncSession, 
    email: str
) -> bool:
    """
    Orquesta el flujo de 'olvidé mi contraseña':
    1. Busca al usuario.
    2. Genera el token.
    3. Envía el email en segundo plano.
    """
    user = await get_user_by_email(db_session, email=email)
    
    # Por seguridad, si el usuario no existe, devolvemos True 
    # para no dar pistas de qué emails están registrados.
    if not user:
        logger.warning(f"Intento de recuperación de contraseña para email no registrado: {email}")
        return True

    try:
        # 1. Generar el token (esto ya hace commit según tu función)
        token = await generate_password_reset_token(db_session, user)
        
        # 2. Enviar el email directamente ya que process_forgot_password corre en BackgroundTasks
        await email_service.send_password_reset_email(
            email=user.email,
            token=token,
            user_name=user.first_name or user.username or user.email
        )
        
        return True
    except Exception as e:
        logger.error(f"Error procesando recuperación de contraseña para {email}: {e}")
        return False