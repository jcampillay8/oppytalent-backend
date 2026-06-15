from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi.responses import RedirectResponse
from google_auth_oauthlib.flow import Flow

from app.database import get_db
from app.dependencies import get_current_user
from app.config import settings
from app.models.usuario import Usuario

router = APIRouter(prefix="/storage", tags=["storage"])

def get_google_drive_flow():
    client_config = {
        "web": {
            "client_id": settings.GOOGLE_CLIENT_ID,
            "client_secret": settings.GOOGLE_CLIENT_SECRET,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "redirect_uris": ["http://localhost:8000/api/v1/storage/google/callback"]
        }
    }
    return Flow.from_client_config(
        client_config,
        scopes=[
            "openid",
            "https://www.googleapis.com/auth/userinfo.email",
            "https://www.googleapis.com/auth/userinfo.profile",
            "https://www.googleapis.com/auth/drive.file"
        ],
        redirect_uri="http://localhost:8000/api/v1/storage/google/callback"
    )

@router.get("/google/login")
async def google_drive_login(current_user=Depends(get_current_user)):
    """Generates the Google OAuth authorization URL for Drive access"""
    if not settings.GOOGLE_CLIENT_ID:
        raise HTTPException(status_code=500, detail="Google OAuth not configured")
        
    from urllib.parse import urlencode
    
    # Generar la URL de autorización manualmente para evitar problemas de estado PKCE
    params = {
        "client_id": settings.GOOGLE_CLIENT_ID,
        "redirect_uri": "http://localhost:8000/api/v1/storage/google/callback",
        "response_type": "code",
        "scope": "openid https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/drive.file",
        "access_type": "offline",
        "prompt": "consent",
        "login_hint": current_user.email,
        "state": current_user.username
    }
    
    auth_url = f"https://accounts.google.com/o/oauth2/auth?{urlencode(params)}"
    return {"auth_url": auth_url}

@router.get("/google/callback")
async def google_drive_callback(code: str, state: str, db: AsyncSession = Depends(get_db)):
    """Handles the Google OAuth callback and saves the refresh token"""
    try:
        # Intercambiar código por tokens
        import httpx
        token_url = "https://oauth2.googleapis.com/token"
        data = {
            "code": code,
            "client_id": settings.GOOGLE_CLIENT_ID,
            "client_secret": settings.GOOGLE_CLIENT_SECRET,
            "redirect_uri": "http://localhost:8000/api/v1/storage/google/callback",
            "grant_type": "authorization_code",
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(token_url, data=data)
            tokens = response.json()
            
        if "error" in tokens:
            raise Exception(f"Error de Google: {tokens.get('error_description', tokens.get('error'))}")
            
        access_token = tokens.get("access_token")
        refresh_token = tokens.get("refresh_token")
        expiry = tokens.get("expires_in") # esto habría que sumarlo a datetime.utcnow(), pero para simplificar lo ignoramos o lo guardamos si lo usamos.
        
        username = state
        print(f"Buscando usuario con username: {username}")
        
        stmt = select(Usuario).where(Usuario.username == username)
        result = await db.execute(stmt)
        user = result.scalar_one_or_none()
        
        print(f"Usuario encontrado: {user}")
        if not user:
            print("ERROR: Usuario no encontrado!")
            raise Exception("Usuario no encontrado")
        
        print(f"REFRESH TOKEN: {refresh_token}", flush=True)
        
        if not refresh_token and not user.google_refresh_token:
            print("ERROR: Google NO envió el Refresh Token!", flush=True)
            from fastapi.responses import JSONResponse
            return JSONResponse(status_code=400, content={"error": "Google no envió el Refresh Token. Revoca el acceso en tu cuenta de Google e inténtalo de nuevo."})
        
        user.google_access_token = access_token
        user.google_refresh_token = refresh_token or user.google_refresh_token
        # user.google_token_expiry = ... omitido por simplicidad, no es estrictamente necesario para la API de python si se maneja bien
        
        await db.commit()
        # Redirigimos al frontend
        redirect_url = f"{settings.WEBSITE_URL}/{username}/almacenamiento?connected=true"
        return RedirectResponse(url=redirect_url)
    except Exception as e:
        print(f"EXCEPTION OCURRED IN CALLBACK: {str(e)}", flush=True)
        import traceback
        traceback.print_exc()
        redirect_url = f"{settings.WEBSITE_URL}?error={str(e)}"
        return RedirectResponse(url=redirect_url)
