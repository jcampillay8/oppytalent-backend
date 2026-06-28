from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_user
from app.models.reconocimiento import Reconocimiento
from app.schemas.reconocimiento import ReconocimientoCreate, ReconocimientoOut, ReconocimientoUpdate
from app.services.crud import get_all, get_by_id, create, update, soft_delete
from app.services.cache import clear_ai_context
from app.models.networking import FeedEvent, FeedEventType

router = APIRouter(prefix="/reconocimientos", tags=["reconocimientos"])

@router.get("/", response_model=list[ReconocimientoOut])
async def list_reconocimientos(username: str | None = None, db: AsyncSession = Depends(get_db)):
    filters = {}
    if username:
        from sqlalchemy import select as sa_select, or_
        from app.models.usuario import Usuario
        result = await db.execute(sa_select(Usuario).where(
            or_(
                Usuario.custom_slug == username,
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

    return await get_all(db, Reconocimiento, filters=filters)

@router.get("/{item_id}", response_model=ReconocimientoOut)
async def get_reconocimiento(item_id: UUID, db: AsyncSession = Depends(get_db)):
    item = await get_by_id(db, Reconocimiento, item_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reconocimiento not found")
    return item

@router.post("/", response_model=ReconocimientoOut, status_code=status.HTTP_201_CREATED)
async def create_reconocimiento(
    body: ReconocimientoCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    data = body.model_dump()
    data["usuario_id"] = current_user.id
    entity = await create(db, Reconocimiento, data)
    
    feed_event = FeedEvent(
        user_id=current_user.id,
        event_type=FeedEventType.NEW_CERTIFICATION,
        entity_id=entity.id
    )
    db.add(feed_event)
    await db.commit()
    
    await clear_ai_context(current_user.id)
    return entity

@router.put("/{item_id}", response_model=ReconocimientoOut)
async def update_reconocimiento(
    item_id: UUID,
    body: ReconocimientoUpdate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    item = await get_by_id(db, Reconocimiento, item_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reconocimiento not found")
    
    if item.usuario_id != current_user.id and current_user.role != 'ADMIN':
         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")

    from app.services.freemium import check_portfolio_limit
    await check_portfolio_limit(db, current_user, "reconocimientos", item_id=item_id)

    entity = await update(db, item, body.model_dump(exclude_none=True))
    await clear_ai_context(item.usuario_id)
    return entity

@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_reconocimiento(
    item_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    item = await get_by_id(db, Reconocimiento, item_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reconocimiento not found")
        
    if item.usuario_id != current_user.id and current_user.role != 'ADMIN':
         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")

    await soft_delete(db, item)
    await clear_ai_context(item.usuario_id)
