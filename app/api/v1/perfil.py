from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_user
from app.models.perfil import Perfil
from app.schemas.perfil import PerfilCreate, PerfilOut, PerfilUpdate
from app.services.crud import get_all, get_by_id, create, update, soft_delete
from app.services.json_sync import sync_all_json

router = APIRouter(prefix="/perfil", tags=["perfil"])


@router.get("/", response_model=list[PerfilOut])
async def list_perfiles(
    username: str | None = None,
    db: AsyncSession = Depends(get_db)
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

    return await get_all(db, Perfil, filters=filters)


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
    current_user=Depends(get_current_user),
):
    data = body.model_dump()
    data["usuario_id"] = current_user.id
    entity = await create(db, Perfil, data)
    await sync_all_json(db)
    return entity


@router.put("/{perfil_id}", response_model=PerfilOut)
async def update_perfil(
    perfil_id: int,
    body: PerfilUpdate,
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_user),
):
    perfil = await get_by_id(db, Perfil, perfil_id)
    if not perfil:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Perfil not found")
    entity = await update(db, perfil, body.model_dump(exclude_none=True))
    await sync_all_json(db)
    return entity


@router.delete("/{perfil_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_perfil(
    perfil_id: int,
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_user),
):
    perfil = await get_by_id(db, Perfil, perfil_id)
    if not perfil:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Perfil not found")
    await soft_delete(db, perfil)
    await sync_all_json(db)
