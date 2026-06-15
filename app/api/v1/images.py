from urllib.parse import quote, unquote

import httpx
from fastapi import APIRouter, HTTPException, Query, UploadFile, File, Depends
from fastapi.responses import Response
from app.dependencies import get_current_user
from app.models.usuario import Usuario
from app.services.cloud_storage import upload_to_r2, upload_to_google_drive

router = APIRouter(tags=["images"])

PROXY_BASE = "/api/v1/images/proxy"


def to_proxy_url(value: str) -> str:
    if PROXY_BASE in value:
        return value
    return f"{PROXY_BASE}?url={quote(value, safe='')}"


@router.get("/proxy")
async def proxy_image(url: str = Query(...)):
    decoded = unquote(url)
    async with httpx.AsyncClient(follow_redirects=True, timeout=30) as client:
        resp = await client.get(
            decoded,
            headers={
                "User-Agent": "Mozilla/5.0 (compatible; PortafolioBot/1.0)",
            },
        )
        if resp.status_code != 200:
            raise HTTPException(
                status_code=resp.status_code,
                detail=f"Failed to fetch image: {resp.status_code}",
            )
        content_type = resp.headers.get("content-type", "image/jpeg")
        return Response(content=resp.content, media_type=content_type)


@router.post("/upload")
async def upload_image(
    file: UploadFile = File(...),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Sube una imagen. Si el usuario es Premium, la sube a Cloudflare R2.
    Si no es Premium, la sube a su Google Drive conectado.
    """
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="El archivo debe ser una imagen")
        
    content = await file.read()
    
    if current_user.is_premium:
        # Premium: Cloudflare R2
        try:
            url = await upload_to_r2(content, file.filename, file.content_type)
            return {"url": url, "source": "r2"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error subiendo imagen premium: {str(e)}")
    else:
        # Free Tier: Google Drive
        if not current_user.google_refresh_token:
            raise HTTPException(
                status_code=403, 
                detail="Debes conectar tu cuenta de Google Drive para subir imágenes gratis, o hacerte Premium."
            )
        try:
            url = await upload_to_google_drive(current_user, content, file.filename, file.content_type)
            return {"url": url, "source": "drive"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error subiendo a Google Drive: {str(e)}")
