from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_user
from app.models.proyecto import Proyecto
from app.schemas.proyecto import ProyectoCreate, ProyectoOut, ProyectoUpdate
from app.services.crud import get_all, get_by_id, create, update, soft_delete
from app.services.cache import get_cached_json, set_cached_json, clear_cache_namespace, clear_ai_context
from app.models.networking import FeedEvent, FeedEventType

router = APIRouter(prefix="/proyectos", tags=["proyectos"])


from fastapi import APIRouter, Depends, HTTPException, status, Query

@router.get("/", response_model=list[ProyectoOut])
async def list_proyectos(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    tag: str | None = None,
    username: str | None = None,
    db: AsyncSession = Depends(get_db),
):
    cache_key = f"api:proyectos:all:{skip}:{limit}:{tag}:{username}"
    cached_data = await get_cached_json(cache_key)
    if cached_data is not None:
        return cached_data

    filters = {}
    if tag:
        filters["tags"] = [tag]
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

    data = await get_all(db, Proyecto, skip=skip, limit=limit, filters=filters)
    await set_cached_json(cache_key, data)
    return data


@router.get("/{proyecto_id}", response_model=ProyectoOut)
async def get_proyecto(proyecto_id: UUID, db: AsyncSession = Depends(get_db)):
    cache_key = f"api:proyectos:{proyecto_id}"
    cached_data = await get_cached_json(cache_key)
    if cached_data is not None:
        return cached_data

    proyecto = await get_by_id(db, Proyecto, proyecto_id)
    if not proyecto:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Proyecto not found")
    
    await set_cached_json(cache_key, proyecto)
    return proyecto


@router.post("/", response_model=ProyectoOut, status_code=status.HTTP_201_CREATED)
async def create_proyecto(
    body: ProyectoCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    data = body.model_dump()
    data["usuario_id"] = current_user.id
    entity = await create(db, Proyecto, data)
    
    # Generate Feed Event
    feed_event = FeedEvent(
        user_id=current_user.id,
        event_type=FeedEventType.NEW_PROJECT,
        entity_id=entity.id
    )
    db.add(feed_event)
    await db.commit()
    
    await clear_cache_namespace("api:proyectos")
    await clear_ai_context(current_user.id)
    return entity


@router.put("/{proyecto_id}", response_model=ProyectoOut)
async def update_proyecto(
    proyecto_id: UUID,
    body: ProyectoUpdate,
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_user),
):
    proyecto = await get_by_id(db, Proyecto, proyecto_id)
    if not proyecto:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Proyecto not found")
        
    from app.services.freemium import check_portfolio_limit
    await check_portfolio_limit(db, current_user, "proyectos", item_id=proyecto_id)
    
    entity = await update(db, proyecto, body.model_dump(exclude_none=True))
    await clear_cache_namespace("api:proyectos")
    await clear_ai_context(proyecto.usuario_id)
    return entity


@router.delete("/{proyecto_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_proyecto(
    proyecto_id: UUID,
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_user),
):
    proyecto = await get_by_id(db, Proyecto, proyecto_id)
    if not proyecto:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Proyecto not found")
    await soft_delete(db, proyecto)
    await clear_cache_namespace("api:proyectos")
    await clear_ai_context(proyecto.usuario_id)
