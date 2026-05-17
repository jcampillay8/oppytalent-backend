from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_admin_user
from app.models.experiencia import Experiencia
from app.schemas.experiencia import ExperienciaCreate, ExperienciaOut, ExperienciaUpdate
from app.services.crud import get_all, get_by_id, create, update, soft_delete
from app.services.json_sync import sync_all_json

router = APIRouter(prefix="/experiencias", tags=["experiencias"])


@router.get("/", response_model=list[ExperienciaOut])
async def list_experiencias(
    skip: int = 0,
    limit: int = 100,
    tag: str | None = None,
    db: AsyncSession = Depends(get_db),
):
    filters = None
    if tag:
        filters = {"tags_industria": [tag]}
    return await get_all(db, Experiencia, skip=skip, limit=limit, filters=filters)


@router.get("/{experiencia_id}", response_model=ExperienciaOut)
async def get_experiencia(experiencia_id: int, db: AsyncSession = Depends(get_db)):
    exp = await get_by_id(db, Experiencia, experiencia_id)
    if not exp:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Experiencia not found")
    return exp


@router.post("/", response_model=ExperienciaOut, status_code=status.HTTP_201_CREATED)
async def create_experiencia(
    body: ExperienciaCreate,
    db: AsyncSession = Depends(get_db),
    _=Depends(get_admin_user),
):
    entity = await create(db, Experiencia, body.model_dump())
    await sync_all_json(db)
    return entity


@router.put("/{experiencia_id}", response_model=ExperienciaOut)
async def update_experiencia(
    experiencia_id: int,
    body: ExperienciaUpdate,
    db: AsyncSession = Depends(get_db),
    _=Depends(get_admin_user),
):
    exp = await get_by_id(db, Experiencia, experiencia_id)
    if not exp:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Experiencia not found")
    entity = await update(db, exp, body.model_dump(exclude_none=True))
    await sync_all_json(db)
    return entity


@router.delete("/{experiencia_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_experiencia(
    experiencia_id: int,
    db: AsyncSession = Depends(get_db),
    _=Depends(get_admin_user),
):
    exp = await get_by_id(db, Experiencia, experiencia_id)
    if not exp:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Experiencia not found")
    await soft_delete(db, exp)
    await sync_all_json(db)
