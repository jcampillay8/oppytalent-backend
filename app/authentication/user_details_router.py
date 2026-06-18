from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated, Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select as sa_select

from app.models import Usuario
from app.dependencies import get_current_user
from app.database import get_db

user_details_router = APIRouter(prefix="/user", tags=["Usuario Details"])

@user_details_router.get("/search")
async def search_users(
    q: str,
    db_session: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[Usuario, Depends(get_current_user)],
):
    from sqlalchemy import or_, func
    
    search_term = f"%{q}%"
    query = (
        sa_select(Usuario)
        .where(
            or_(
                Usuario.first_name.ilike(search_term),
                Usuario.last_name.ilike(search_term),
                Usuario.username.ilike(search_term),
                func.concat(Usuario.first_name, ' ', Usuario.last_name).ilike(search_term)
            )
        )
        .limit(20)
    )
    result = await db_session.execute(query)
    users = result.scalars().all()
    
    # Mapeo manual para evitar esquemas complejos heredados
    return [
        {
            "id": u.id,
            "username": u.username,
            "firstName": u.first_name,
            "lastName": u.last_name,
            "userImage": getattr(u, 'avatar_url', None) or getattr(u, 'user_image', None),
            "occupation": "Talento OppyTalent" # Hardcoded temporalmente
        }
        for u in users
    ]

@user_details_router.get("/profile")
async def read_current_user_profile(
    current_user: Annotated[Usuario, Depends(get_current_user)],
):
    # Ya que dependemos de get_current_user, el usuario ya ha sido extraído y validado por token
    return {
        "id": current_user.id,
        "username": current_user.username.split('@')[0],
        "email": current_user.email,
        "firstName": current_user.first_name,
        "lastName": current_user.last_name,
        "userImage": getattr(current_user, 'avatar_url', None) or getattr(current_user, 'user_image', None),
        "occupation": "Talento OppyTalent", # Hardcoded temporalmente
        "roles": [], # Se añadirá si es necesario en un futuro
        "chat_welcome_message": current_user.chat_welcome_message,
        "chat_suggested_q1": current_user.chat_suggested_q1,
        "chat_suggested_q3": current_user.chat_suggested_q3,
        "portfolio_theme": current_user.portfolio_theme or "dark-glass",
        "portfolio_layout": current_user.portfolio_layout or "tabs",
        "google_refresh_token": bool(current_user.google_refresh_token),
        "is_premium": getattr(current_user, 'is_premium', False),
        "has_gemini_key": bool(getattr(current_user, 'encrypted_gemini_key', None)),
        "ai_credits": getattr(current_user, 'ai_credits', 0)
    }
    
from pydantic import BaseModel

class ChatConfigUpdate(BaseModel):
    chat_welcome_message: Optional[str] = None
    chat_suggested_q1: Optional[str] = None
    chat_suggested_q2: Optional[str] = None
    chat_suggested_q3: Optional[str] = None

@user_details_router.put("/chat-config")
async def update_chat_config(
    body: ChatConfigUpdate,
    current_user: Annotated[Usuario, Depends(get_current_user)],
    db_session: Annotated[AsyncSession, Depends(get_db)],
):
    if body.chat_welcome_message is not None:
        current_user.chat_welcome_message = body.chat_welcome_message
    if body.chat_suggested_q1 is not None:
        current_user.chat_suggested_q1 = body.chat_suggested_q1
    if body.chat_suggested_q2 is not None:
        current_user.chat_suggested_q2 = body.chat_suggested_q2
    if body.chat_suggested_q3 is not None:
        current_user.chat_suggested_q3 = body.chat_suggested_q3
        
    await db_session.commit()
    return {"status": "success", "message": "Chat config updated"}

class ThemeConfigUpdate(BaseModel):
    portfolio_theme: Optional[str] = None
    portfolio_layout: Optional[str] = None

@user_details_router.put("/theme-config")
async def update_theme_config(
    body: ThemeConfigUpdate,
    current_user: Annotated[Usuario, Depends(get_current_user)],
    db_session: Annotated[AsyncSession, Depends(get_db)],
):
    if body.portfolio_theme is not None:
        current_user.portfolio_theme = body.portfolio_theme
    if body.portfolio_layout is not None:
        current_user.portfolio_layout = body.portfolio_layout
        
    await db_session.commit()
    return {
        "status": "success", 
        "message": "Theme config updated", 
        "portfolio_theme": current_user.portfolio_theme,
        "portfolio_layout": current_user.portfolio_layout
    }

class GeminiKeyUpdate(BaseModel):
    api_key: str

@user_details_router.put("/gemini-key")
async def update_gemini_key(
    body: GeminiKeyUpdate,
    current_user: Annotated[Usuario, Depends(get_current_user)],
    db_session: Annotated[AsyncSession, Depends(get_db)],
):
    import google.generativeai as genai
    from app.services.crypto import encrypt_value
    
    # 1. Validate the API Key by making a simple request
    try:
        genai.configure(api_key=body.api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        # Ping the API
        model.generate_content("ping")
    except Exception as e:
        raise HTTPException(status_code=400, detail="La API Key ingresada no es válida o no tiene permisos.")
        
    # 2. Encrypt and save
    try:
        current_user.encrypted_gemini_key = encrypt_value(body.api_key)
        await db_session.commit()
        return {"status": "success", "message": "API Key guardada de forma segura"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al encriptar la llave. Revisa la configuración del servidor.")


@user_details_router.get("/{username}")
async def get_user_by_username(
    username: str,
    db_session: Annotated[AsyncSession, Depends(get_db)],
):
    from sqlalchemy import or_
    # Look up by the prefix or full email since usernames are emails right now
    query = sa_select(Usuario).where(
        or_(
            Usuario.username == username,
            Usuario.email == username,
            Usuario.username.ilike(f"{username}@%")
        )
    )
    result = await db_session.execute(query)
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
    return {
        "id": user.id,
        "username": user.username.split('@')[0],
        "firstName": user.first_name,
        "lastName": user.last_name,
        "userImage": getattr(user, 'avatar_url', None) or getattr(user, 'user_image', None),
        "occupation": "Talento OppyTalent",
        "chat_welcome_message": user.chat_welcome_message,
        "chat_suggested_q1": user.chat_suggested_q1,
        "chat_suggested_q2": user.chat_suggested_q2,
        "chat_suggested_q3": user.chat_suggested_q3,
        "portfolio_theme": user.portfolio_theme or "dark-glass",
        "portfolio_layout": user.portfolio_layout or "tabs"
    }