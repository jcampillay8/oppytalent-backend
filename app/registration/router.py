# src/registration/router.py
import logging
from fastapi import APIRouter, Depends, Form, File, UploadFile, HTTPException, status
from fastapi.responses import RedirectResponse, HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.database import get_db
from app.registration import services as reg_services  # módulo
from app.registration.schemas import UsuarioRegisterSchema  # schema

logger = logging.getLogger(__name__)
account_router = APIRouter(tags=["Account Management"])

@account_router.post(
    "/register",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Register a new user and send a confirmation email",
    response_description="A confirmation email has been sent to the user's email address.",
)
async def register_user(
    db_session: AsyncSession = Depends(get_db),
    first_name: str = Form(..., max_length=50),
    last_name: str = Form(..., max_length=50),
    username: str = Form(..., min_length=3, max_length=50),
    email: str = Form(..., max_length=100),
    password: str = Form(..., min_length=8),
    terms_accepted: bool = Form(...),
    referral_code: str | None = Form(None),
    user_image: UploadFile | None = File(None, description="Profile image of the user"),
):
    user_data = UsuarioRegisterSchema(
        first_name=first_name,
        last_name=last_name,
        username=username,
        email=email,
        password=password,
        terms_accepted=terms_accepted,
        referral_code=referral_code,
    )

    # Validación contraseña
    reg_services.validate_password_complexity(user_data.password)

    # Duplicados
    existing_user = await reg_services.get_user_by_email_or_username(
        db_session,
        email=user_data.email.lower(),
        username=user_data.username.lower(),
    )
    if existing_user:
        if existing_user.email == user_data.email.lower():
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Ya existe un usuario con este correo electrónico.")
        if existing_user.username == user_data.username.lower():
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Ya existe un usuario con este nombre de usuario.")

    if not user_data.terms_accepted:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Debes aceptar los Términos y Condiciones para registrarte.")

    # Enviar email de confirmación (incluye lógica de bypass para emails de prueba de MP)
    return await reg_services.register_user_and_send_confirmation( # 👈 LÍNEA CORREGIDA
        db_session=db_session,
        user_schema=user_data,
        uploaded_image=user_image,
    )

from fastapi.responses import RedirectResponse

@account_router.get("/confirm-email/{token}")
async def confirm_email(
    token: str,
    db_session: AsyncSession = Depends(get_db),
):
    # 1. Activamos al usuario en la DB (Esto ya funciona en Neon)
    await reg_services.confirm_user_email(db_session=db_session, token=token)
    
    # 2. Redirección al frontend web
    base = str(settings.WEBSITE_URL).rstrip('/')
    app_url = f"{base}/login?confirmed=true&token={token}"
    
    return RedirectResponse(url=app_url)
