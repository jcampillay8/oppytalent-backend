from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_

from app.database import get_db
from app.models.usuario import Usuario

router = APIRouter()

@router.get("/card/{username}", response_class=HTMLResponse)
async def get_open_graph_card(
    username: str,
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Usuario).where(
            or_(
                Usuario.custom_slug == username,
                Usuario.username == username,
                Usuario.email == username,
                Usuario.username.ilike(f"{username}@%")
            )
        )
    )
    user = result.scalar_one_or_none()
    
    if not user:
        # Fallback default OG tags
        title = "OppyTalent"
        description = "Portafolios profesionales potenciados por Inteligencia Artificial."
        image_url = "https://oppytalent.com/default-og.jpg"
    else:
        name = f"{user.first_name or ''} {user.last_name or ''}".strip() or user.username
        title = f"{name} - Portafolio Profesional"
        description = f"Conoce la experiencia, proyectos y habilidades de {name}. Chatea con su asistente virtual de IA."
        image_url = getattr(user, 'avatar_url', None) or user.user_image or "https://oppytalent.com/default-og.jpg"

    # La URL base del frontend
    frontend_url = f"http://localhost:5173/{username}"
    
    html_content = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>{title}</title>
        
        <!-- Open Graph / Facebook / LinkedIn / WhatsApp -->
        <meta property="og:type" content="website">
        <meta property="og:url" content="{frontend_url}">
        <meta property="og:title" content="{title}">
        <meta property="og:description" content="{description}">
        <meta property="og:image" content="{image_url}">
        
        <!-- Twitter -->
        <meta name="twitter:card" content="summary_large_image">
        <meta name="twitter:title" content="{title}">
        <meta name="twitter:description" content="{description}">
        <meta name="twitter:image" content="{image_url}">
        
        <!-- Redirect para navegadores reales -->
        <meta http-equiv="refresh" content="0; url={frontend_url}">
        <script>
            window.location.replace("{frontend_url}");
        </script>
    </head>
    <body>
        <p>Redirigiendo al portafolio de {title}...</p>
        <a href="{frontend_url}">Haz clic aquí si no eres redirigido automáticamente</a>
    </body>
    </html>
    """
    
    return HTMLResponse(content=html_content)
