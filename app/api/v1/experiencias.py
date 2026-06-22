from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_user
from app.models.experiencia import Experiencia
from app.schemas.experiencia import ExperienciaCreate, ExperienciaOut, ExperienciaUpdate
from app.services.crud import get_all, get_by_id, create, update, soft_delete
from app.services.cache import get_cached_json, set_cached_json, clear_cache_namespace, clear_ai_context

router = APIRouter(prefix="/experiencias", tags=["experiencias"])


@router.get("/", response_model=list[ExperienciaOut])
async def list_experiencias(
    skip: int = 0,
    limit: int = 100,
    tag: str | None = None,
    username: str | None = None,
    db: AsyncSession = Depends(get_db),
):
    cache_key = f"api:experiencias:all:{skip}:{limit}:{tag}:{username}"
    cached_data = await get_cached_json(cache_key)
    if cached_data is not None:
        return cached_data

    filters = {}
    if tag:
        filters["tags_industria"] = [tag]
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

    data = await get_all(db, Experiencia, skip=skip, limit=limit, filters=filters)
    await set_cached_json(cache_key, data)
    return data


@router.get("/{experiencia_id}", response_model=ExperienciaOut)
async def get_experiencia(experiencia_id: UUID, db: AsyncSession = Depends(get_db)):
    cache_key = f"api:experiencias:{experiencia_id}"
    cached_data = await get_cached_json(cache_key)
    if cached_data is not None:
        return cached_data

    exp = await get_by_id(db, Experiencia, experiencia_id)
    if not exp:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Experiencia not found")
    
    await set_cached_json(cache_key, exp)
    return exp


@router.post("/", response_model=ExperienciaOut, status_code=status.HTTP_201_CREATED)
async def create_experiencia(
    body: ExperienciaCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    data = body.model_dump()
    data["usuario_id"] = current_user.id
    entity = await create(db, Experiencia, data)
    await clear_cache_namespace("api:experiencias")
    await clear_ai_context(current_user.id)
    return entity


@router.put("/{experiencia_id}", response_model=ExperienciaOut)
async def update_experiencia(
    experiencia_id: UUID,
    body: ExperienciaUpdate,
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_user),
):
    exp = await get_by_id(db, Experiencia, experiencia_id)
    if not exp:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Experiencia not found")
    entity = await update(db, exp, body.model_dump(exclude_none=True))
    await clear_cache_namespace("api:experiencias")
    await clear_ai_context(exp.usuario_id)
    return entity


@router.delete("/{experiencia_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_experiencia(
    experiencia_id: UUID,
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_user),
):
    exp = await get_by_id(db, Experiencia, experiencia_id)
    if not exp:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Experiencia not found")
    await soft_delete(db, exp)
    await clear_cache_namespace("api:experiencias")
    await clear_ai_context(exp.usuario_id)
