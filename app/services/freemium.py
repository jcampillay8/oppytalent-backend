from uuid import UUID
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.usuario import Usuario
from app.models.experiencia import Experiencia
from app.models.proyecto import Proyecto
from app.models.estudio import Estudio
from app.models.reconocimiento import Reconocimiento
from app.models.habilitacion import Habilitacion

CATEGORY_MODELS = {
    "experiencias": Experiencia,
    "proyectos": Proyecto,
    "estudios": Estudio,
    "reconocimientos": Reconocimiento,
    "habilitaciones": Habilitacion
}

def get_tier_limit(tier: str) -> int:
    limits = {
        "BASIC": 2,
        "PRO": 4,
        "PREMIUM": 6,
        "AMBASSADOR": 8,
        "PROFESSIONAL": 9999,
        "BYOK": 9999
    }
    return limits.get(tier.upper(), 2)

def get_skills_limit(tier: str) -> int:
    limits = {
        "BASIC": 0,
        "PRO": 2,
        "PREMIUM": 3,
        "AMBASSADOR": 5,
        "PROFESSIONAL": 9999,
        "BYOK": 9999
    }
    return limits.get(tier.upper(), 0)

async def check_portfolio_limit(db: AsyncSession, current_user: Usuario, category: str, item_id: UUID = None):
    """
    If item_id is None, it means the user is trying to CREATE a new item. We check if they exceed the max allowed.
    If item_id is provided, it means they are trying to UPDATE. We check if this item's index is within the allowed limit.
    """
    model = CATEGORY_MODELS.get(category)
    if not model:
        return
    
    tier = getattr(current_user, "freemium_tier", "BASIC")
    if tier.upper() == "ADMIN": # Override for admins if needed
        return

    limit = get_tier_limit(tier)

    # Fetch all items of this user for this category to determine count and index
    stmt = select(model).where(
        model.usuario_id == current_user.id,
        model.is_active == True,
        model.is_deleted == False
    ).order_by(model.created_at.desc())
    
    result = await db.execute(stmt)
    items = result.scalars().all()
    
    if item_id is None:
        # Creating a new item manually
        if len(items) >= limit:
            raise HTTPException(
                status_code=403, 
                detail=f"Límite alcanzado. Tu plan Freemium ({tier}) permite un máximo de {limit} elementos en esta categoría. Cumple una misión social para desbloquear tu portafolio."
            )
    else:
        # Updating an existing item
        for i, item in enumerate(items):
            if str(item.id) == str(item_id):
                if i >= limit:
                    raise HTTPException(
                        status_code=403, 
                        detail=f"Este registro está bloqueado. Tu plan Freemium ({tier}) permite editar solo los últimos {limit} elementos. Desbloquea la edición completando una misión social gratis."
                    )
                return
