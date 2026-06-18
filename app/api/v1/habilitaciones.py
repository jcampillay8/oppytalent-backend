from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_user
from app.models.habilitacion import Habilitacion
from app.schemas.habilitacion import HabilitacionCreate, HabilitacionOut, HabilitacionUpdate
from app.services.crud import get_all, get_by_id, create, update, soft_delete
from app.services.cache import clear_ai_context

router = APIRouter(prefix="/habilitaciones", tags=["habilitaciones"])

@router.get("/", response_model=list[HabilitacionOut])
async def list_habilitaciones(username: str | None = None, db: AsyncSession = Depends(get_db)):
    filters = {}
    if username:
        from sqlalchemy import select as sa_select, or_
        from app.models.usuario import Usuario
        result = await db.execute(sa_select(Usuario).where(
            or_(
                Usuario.username == username,
                Usuario.email == username,
                Usuario.username.ilike(f"{username}@%")
            )
        ))
        user = result.scalar_one_or_none()
        if user:
            filters["usuario_id"] = user.id
        else:
            return []

    return await get_all(db, Habilitacion, filters=filters)

@router.get("/{item_id}", response_model=HabilitacionOut)
async def get_habilitacion(item_id: int, db: AsyncSession = Depends(get_db)):
    item = await get_by_id(db, Habilitacion, item_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Habilitacion not found")
    return item

@router.post("/", response_model=HabilitacionOut, status_code=status.HTTP_201_CREATED)
async def create_habilitacion(
    body: HabilitacionCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    data = body.model_dump()
    data["usuario_id"] = current_user.id
    entity = await create(db, Habilitacion, data)
    await clear_ai_context(current_user.id)
    return entity

@router.put("/{item_id}", response_model=HabilitacionOut)
async def update_habilitacion(
    item_id: int,
    body: HabilitacionUpdate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    item = await get_by_id(db, Habilitacion, item_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Habilitacion not found")
    
    if item.usuario_id != current_user.id and current_user.role != 'ADMIN':
         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")

    entity = await update(db, item, body.model_dump(exclude_none=True))
    await clear_ai_context(item.usuario_id)
    return entity

@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_habilitacion(
    item_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    item = await get_by_id(db, Habilitacion, item_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Habilitacion not found")
        
    if item.usuario_id != current_user.id and current_user.role != 'ADMIN':
         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")

    await soft_delete(db, item)
    await clear_ai_context(item.usuario_id)
