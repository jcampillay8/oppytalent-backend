from urllib.parse import quote, unquote

import httpx
from fastapi import APIRouter, HTTPException, Query, UploadFile, File, Depends
from fastapi.responses import Response
from app.dependencies import get_current_user, get_db
from app.models.usuario import Usuario
from app.services.cloud_storage import upload_to_r2
from sqlalchemy.ext.asyncio import AsyncSession

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
    current_user: Usuario = Depends(get_current_user),
    db_session: AsyncSession = Depends(get_db)
):
    """
    Sube una imagen a Cloudflare R2 con control de cuota.
    Free tier: 20 MB. Premium: Ilimitado.
    """
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="El archivo debe ser una imagen")
        
    content = await file.read()
    file_size = len(content)
    
    # Validación de Cuota (25 MB) para usuarios no premium
    if not current_user.is_premium:
        if current_user.storage_used + file_size > 26_214_400:
            raise HTTPException(
                status_code=402, 
                detail="Has alcanzado tu límite gratuito de 25 MB. Sube a Premium para obtener almacenamiento de 1 GB, analíticas de chat y diseños exclusivos."
            )
            
    # Subir a R2 (único proveedor de almacenamiento)
    try:
        url = await upload_to_r2(content, file.filename, file.content_type)
        
        # Actualizar cuota usada en BD
        current_user.storage_used += file_size
        db_session.add(current_user)
        await db_session.commit()
        
        return {"url": url, "source": "r2"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error subiendo imagen: {str(e)}")
