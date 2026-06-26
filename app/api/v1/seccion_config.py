from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from app.database import get_db
from app.models.seccion_config import SeccionConfig
from app.schemas.seccion_config import SeccionConfigResponse, SeccionConfigCreate, SeccionConfigUpdate
from app.dependencies import get_current_user

router = APIRouter()

@router.get("/", response_model=List[SeccionConfigResponse])
async def get_seccion_configs(
    username: str | None = None,
    db: AsyncSession = Depends(get_db)
):
    user_id = None
    if username:
        from app.models.usuario import Usuario
        from sqlalchemy import or_
        result = await db.execute(select(Usuario).where(
            or_(
                Usuario.custom_slug == username,
                Usuario.username == username,
                Usuario.email == username,
                Usuario.username.ilike(f"{username}@%")
            )
        ))
        user = result.scalar_one_or_none()
        if user:
            user_id = user.id

    if not user_id:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    result = await db.execute(select(SeccionConfig).where(SeccionConfig.usuario_id == user_id))
    configs = result.scalars().all()
    
    if not configs:
        # Initialize defaults
        default_configs = [
            SeccionConfig(usuario_id=user_id, seccion='tags', is_expanded=False),
            SeccionConfig(usuario_id=user_id, seccion='proyectos', is_expanded=True),
            SeccionConfig(usuario_id=user_id, seccion='experiencia', is_expanded=True),
            SeccionConfig(usuario_id=user_id, seccion='estudios', is_expanded=True),
        ]
        db.add_all(default_configs)
        await db.commit()
        
        result = await db.execute(select(SeccionConfig).where(SeccionConfig.usuario_id == user_id))
        configs = result.scalars().all()
        
    return configs

@router.put("/{seccion}", response_model=SeccionConfigResponse)
async def update_seccion_config(
    seccion: str, 
    config_data: SeccionConfigUpdate, 
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    result = await db.execute(
        select(SeccionConfig)
        .where(SeccionConfig.seccion == seccion)
        .where(SeccionConfig.usuario_id == current_user.id)
    )
    config = result.scalar_one_or_none()
    
    if not config:
        # Create if it doesn't exist
        config = SeccionConfig(usuario_id=current_user.id, seccion=seccion, is_expanded=config_data.is_expanded)
        db.add(config)
    else:
        config.is_expanded = config_data.is_expanded
        
    await db.commit()
    await db.refresh(config)
    return config
