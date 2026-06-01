from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from app.database import get_db
from app.models.seccion_config import SeccionConfig
from app.schemas.seccion_config import SeccionConfigResponse, SeccionConfigCreate, SeccionConfigUpdate
from app.dependencies import get_admin_user

router = APIRouter()

@router.get("/", response_model=List[SeccionConfigResponse])
async def get_seccion_configs(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(SeccionConfig))
    configs = result.scalars().all()
    
    if not configs:
        # Initialize defaults
        default_configs = [
            SeccionConfig(seccion='tags', is_expanded=False),
            SeccionConfig(seccion='proyectos', is_expanded=True),
            SeccionConfig(seccion='experiencia', is_expanded=True),
            SeccionConfig(seccion='estudios', is_expanded=True),
        ]
        db.add_all(default_configs)
        await db.commit()
        
        result = await db.execute(select(SeccionConfig))
        configs = result.scalars().all()
        
    return configs

@router.put("/{seccion}", response_model=SeccionConfigResponse)
async def update_seccion_config(
    seccion: str, 
    config_data: SeccionConfigUpdate, 
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_admin_user)
):
    result = await db.execute(select(SeccionConfig).where(SeccionConfig.seccion == seccion))
    config = result.scalar_one_or_none()
    
    if not config:
        # Create if it doesn't exist
        config = SeccionConfig(seccion=seccion, is_expanded=config_data.is_expanded)
        db.add(config)
    else:
        config.is_expanded = config_data.is_expanded
        
    await db.commit()
    await db.refresh(config)
    return config
