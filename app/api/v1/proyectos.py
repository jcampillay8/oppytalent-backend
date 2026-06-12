from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_user
from app.models.proyecto import Proyecto
from app.schemas.proyecto import ProyectoCreate, ProyectoOut, ProyectoUpdate
from app.services.crud import get_all, get_by_id, create, update, soft_delete
from app.services.json_sync import sync_all_json
from app.services.cache import get_cached_json, set_cached_json, clear_cache_namespace

router = APIRouter(prefix="/proyectos", tags=["proyectos"])


@router.get("/", response_model=list[ProyectoOut])
async def list_proyectos(
    skip: int = 0,
    limit: int = 100,
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
async def get_proyecto(proyecto_id: int, db: AsyncSession = Depends(get_db)):
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
    await sync_all_json(db)
    await clear_cache_namespace("api:proyectos")
    return entity


@router.put("/{proyecto_id}", response_model=ProyectoOut)
async def update_proyecto(
    proyecto_id: int,
    body: ProyectoUpdate,
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_user),
):
    proyecto = await get_by_id(db, Proyecto, proyecto_id)
    if not proyecto:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Proyecto not found")
    entity = await update(db, proyecto, body.model_dump(exclude_none=True))
    await sync_all_json(db)
    await clear_cache_namespace("api:proyectos")
    return entity


@router.delete("/{proyecto_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_proyecto(
    proyecto_id: int,
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_user),
):
    proyecto = await get_by_id(db, Proyecto, proyecto_id)
    if not proyecto:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Proyecto not found")
    await soft_delete(db, proyecto)
    await sync_all_json(db)
    await clear_cache_namespace("api:proyectos")
