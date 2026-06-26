from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_user
from app.models.estudio import Estudio
from app.schemas.estudio import EstudioCreate, EstudioOut, EstudioUpdate
from app.services.crud import get_all, get_by_id, create, update, soft_delete
from app.services.cache import clear_ai_context
from app.models.networking import FeedEvent, FeedEventType

router = APIRouter(prefix="/estudios", tags=["estudios"])


@router.get("/", response_model=list[EstudioOut])
async def list_estudios(
    skip: int = 0,
    limit: int = 100,
    username: str | None = None,
    db: AsyncSession = Depends(get_db),
):
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

    return await get_all(db, Estudio, skip=skip, limit=limit, filters=filters)


@router.get("/{estudio_id}", response_model=EstudioOut)
async def get_estudio(estudio_id: UUID, db: AsyncSession = Depends(get_db)):
    estudio = await get_by_id(db, Estudio, estudio_id)
    if not estudio:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Estudio not found")
    return estudio


@router.post("/", response_model=EstudioOut, status_code=status.HTTP_201_CREATED)
async def create_estudio(
    body: EstudioCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    data = body.model_dump()
    data["usuario_id"] = current_user.id
    entity = await create(db, Estudio, data)
    
    feed_event = FeedEvent(
        user_id=current_user.id,
        event_type=FeedEventType.NEW_STUDY,
        entity_id=entity.id
    )
    db.add(feed_event)
    await db.commit()
    
    await clear_ai_context(current_user.id)
    return entity


@router.put("/{estudio_id}", response_model=EstudioOut)
async def update_estudio(
    estudio_id: UUID,
    body: EstudioUpdate,
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_user),
):
    estudio = await get_by_id(db, Estudio, estudio_id)
    if not estudio:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Estudio not found")
    entity = await update(db, estudio, body.model_dump(exclude_none=True))
    await clear_ai_context(estudio.usuario_id)
    return entity


@router.delete("/{estudio_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_estudio(
    estudio_id: UUID,
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_user),
):
    estudio = await get_by_id(db, Estudio, estudio_id)
    if not estudio:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Estudio not found")
    await soft_delete(db, estudio)
    await clear_ai_context(estudio.usuario_id)

