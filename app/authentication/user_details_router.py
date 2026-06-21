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
    from sqlalchemy.orm import outerjoin
    from app.models.perfil import Perfil
    
    search_term = f"%{q}%"
    query = (
        sa_select(Usuario, Perfil)
        .outerjoin(Perfil, Usuario.id == Perfil.usuario_id)
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
    rows = result.all()
    
    return [
        {
            "id": u.id,
            "username": u.username,
            "firstName": p.nombre_completo if p and p.nombre_completo else u.first_name,
            "lastName": "" if (p and p.nombre_completo) else u.last_name,
            "userImage": p.avatar_url if p and p.avatar_url else u.user_image,
            "occupation": p.ocupacion if p and p.ocupacion else "Talento OppyTalent"
        }
        for u, p in rows
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
        "ai_pitch_rules": getattr(current_user, 'ai_pitch_rules', []),
        "portfolio_theme": current_user.portfolio_theme or "dark-glass",
        "portfolio_layout": current_user.portfolio_layout or "tabs",
        "google_refresh_token": bool(current_user.google_refresh_token),
        "is_premium": getattr(current_user, 'is_premium', False),
        "has_gemini_key": bool(getattr(current_user, 'encrypted_gemini_key', None)),
        "ai_credits": getattr(current_user, 'ai_credits', 0),
        "storage_used": getattr(current_user, 'storage_used', 0),
        "is_visible_b2b": getattr(current_user, 'is_visible_b2b', False),
        "is_recruiter": getattr(current_user, 'is_recruiter', False)
    }
    
from pydantic import BaseModel

class ChatConfigUpdate(BaseModel):
    chat_welcome_message: Optional[str] = None
    ai_pitch_rules: Optional[list] = None

@user_details_router.put("/chat-config")
async def update_chat_config(
    body: ChatConfigUpdate,
    current_user: Annotated[Usuario, Depends(get_current_user)],
    db_session: Annotated[AsyncSession, Depends(get_db)],
):
    if body.chat_welcome_message is not None:
        current_user.chat_welcome_message = body.chat_welcome_message
    if body.ai_pitch_rules is not None:
        current_user.ai_pitch_rules = body.ai_pitch_rules
        
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

class B2BConfigUpdate(BaseModel):
    is_visible_b2b: Optional[bool] = None

@user_details_router.put("/b2b-config")
async def update_b2b_config(
    body: B2BConfigUpdate,
    current_user: Annotated[Usuario, Depends(get_current_user)],
    db_session: Annotated[AsyncSession, Depends(get_db)],
):
    if body.is_visible_b2b is not None:
        current_user.is_visible_b2b = body.is_visible_b2b
        
    await db_session.commit()
    return {"status": "success", "message": "B2B config updated", "is_visible_b2b": current_user.is_visible_b2b}

class GeminiKeyUpdate(BaseModel):
    api_key: str

@user_details_router.put("/gemini-key")
async def update_gemini_key(
    body: GeminiKeyUpdate,
    current_user: Annotated[Usuario, Depends(get_current_user)],
    db_session: Annotated[AsyncSession, Depends(get_db)],
):
    from google import genai
    from app.services.crypto import encrypt_value
    
    # 1. Validate the API Key by making a simple request
    try:
        client = genai.Client(api_key=body.api_key)
        # Ping the API
        client.models.generate_content(
            model='gemini-1.5-flash',
            contents='ping'
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail="La API Key ingresada no es válida o no tiene permisos.")
        
    # 2. Encrypt and save
    try:
        current_user.encrypted_gemini_key = encrypt_value(body.api_key)
        await db_session.commit()
        return {"status": "success", "message": "API Key guardada de forma segura"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al encriptar la llave. Revisa la configuración del servidor.")

class KYCVerification(BaseModel):
    is_recruiter: bool

@user_details_router.put("/kyc/verify-recruiter/{user_id}")
async def verify_recruiter_kyc(
    user_id: int,
    body: KYCVerification,
    current_user: Annotated[Usuario, Depends(get_current_user)],
    db_session: Annotated[AsyncSession, Depends(get_db)],
):
    """
    Endpoint exclusivo para SUPERADMIN.
    Permite validar (KYC) a una empresa y darle acceso de Headhunter.
    """
    if current_user.role != "SUPERADMIN":
        raise HTTPException(status_code=403, detail="Acceso denegado. Solo SUPERADMIN puede verificar empresas.")
        
    user_result = await db_session.execute(sa_select(Usuario).where(Usuario.id == user_id))
    target_user = user_result.scalar_one_or_none()
    
    if not target_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")
        
    target_user.is_recruiter = body.is_recruiter
    await db_session.commit()
    
    status_str = "Aprobada" if body.is_recruiter else "Revocada"
    return {"status": "success", "message": f"Verificación KYC de B2B {status_str} para {target_user.username}"}

@user_details_router.post("/sync-rag")
async def sync_rag_vectors(
    current_user: Annotated[Usuario, Depends(get_current_user)],
    db_session: Annotated[AsyncSession, Depends(get_db)],
):
    from app.ai_management.rag_sync import sync_user_rag_embeddings
    from app.services.crypto import decrypt_value
    
    api_key = None
    if getattr(current_user, 'encrypted_gemini_key', None):
        try:
            api_key = decrypt_value(current_user.encrypted_gemini_key)
        except Exception:
            pass
            
    try:
        count = await sync_user_rag_embeddings(db_session, current_user.id, api_key=api_key)
        return {"status": "success", "message": f"Se sincronizaron {count} documentos al Cerebro IA exitosamente."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al sincronizar vectores: {str(e)}")


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
        "ai_pitch_rules": getattr(user, 'ai_pitch_rules', []),
        "portfolio_theme": user.portfolio_theme or "dark-glass",
        "portfolio_layout": user.portfolio_layout or "tabs"
    }