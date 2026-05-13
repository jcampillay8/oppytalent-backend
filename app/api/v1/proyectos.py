from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_admin_user
from app.models.proyecto import Proyecto
from app.schemas.proyecto import ProyectoCreate, ProyectoOut, ProyectoUpdate
from app.services.crud import get_all, get_by_id, create, update, soft_delete

router = APIRouter(prefix="/proyectos", tags=["proyectos"])


@router.get("/", response_model=list[ProyectoOut])
async def list_proyectos(
    skip: int = 0,
    limit: int = 100,
    tag: str | None = None,
    db: AsyncSession = Depends(get_db),
):
    filters = None
    if tag:
        filters = {"tags": [tag]}
    return await get_all(db, Proyecto, skip=skip, limit=limit, filters=filters)


@router.get("/{proyecto_id}", response_model=ProyectoOut)
async def get_proyecto(proyecto_id: int, db: AsyncSession = Depends(get_db)):
    proyecto = await get_by_id(db, Proyecto, proyecto_id)
    if not proyecto:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Proyecto not found")
    return proyecto


@router.post("/", response_model=ProyectoOut, status_code=status.HTTP_201_CREATED)
async def create_proyecto(
    body: ProyectoCreate,
    db: AsyncSession = Depends(get_db),
    _=Depends(get_admin_user),
):
    return await create(db, Proyecto, body.model_dump())


@router.put("/{proyecto_id}", response_model=ProyectoOut)
async def update_proyecto(
    proyecto_id: int,
    body: ProyectoUpdate,
    db: AsyncSession = Depends(get_db),
    _=Depends(get_admin_user),
):
    proyecto = await get_by_id(db, Proyecto, proyecto_id)
    if not proyecto:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Proyecto not found")
    return await update(db, proyecto, body.model_dump(exclude_none=True))


@router.delete("/{proyecto_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_proyecto(
    proyecto_id: int,
    db: AsyncSession = Depends(get_db),
    _=Depends(get_admin_user),
):
    proyecto = await get_by_id(db, Proyecto, proyecto_id)
    if not proyecto:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Proyecto not found")
    await soft_delete(db, proyecto)
