from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_admin_user
from app.models.perfil import Perfil
from app.schemas.perfil import PerfilCreate, PerfilOut, PerfilUpdate
from app.services.crud import get_all, get_by_id, create, update, soft_delete

router = APIRouter(prefix="/perfil", tags=["perfil"])


@router.get("/", response_model=list[PerfilOut])
async def list_perfiles(db: AsyncSession = Depends(get_db)):
    return await get_all(db, Perfil)


@router.get("/{perfil_id}", response_model=PerfilOut)
async def get_perfil(perfil_id: int, db: AsyncSession = Depends(get_db)):
    perfil = await get_by_id(db, Perfil, perfil_id)
    if not perfil:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Perfil not found")
    return perfil


@router.post("/", response_model=PerfilOut, status_code=status.HTTP_201_CREATED)
async def create_perfil(
    body: PerfilCreate,
    db: AsyncSession = Depends(get_db),
    _=Depends(get_admin_user),
):
    return await create(db, Perfil, body.model_dump())


@router.put("/{perfil_id}", response_model=PerfilOut)
async def update_perfil(
    perfil_id: int,
    body: PerfilUpdate,
    db: AsyncSession = Depends(get_db),
    _=Depends(get_admin_user),
):
    perfil = await get_by_id(db, Perfil, perfil_id)
    if not perfil:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Perfil not found")
    return await update(db, perfil, body.model_dump(exclude_none=True))


@router.delete("/{perfil_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_perfil(
    perfil_id: int,
    db: AsyncSession = Depends(get_db),
    _=Depends(get_admin_user),
):
    perfil = await get_by_id(db, Perfil, perfil_id)
    if not perfil:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Perfil not found")
    await soft_delete(db, perfil)
