from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_user
from app.models.estudio import Estudio
from app.schemas.estudio import EstudioCreate, EstudioOut, EstudioUpdate
from app.services.crud import get_all, get_by_id, create, update, soft_delete
from app.services.json_sync import sync_all_json

router = APIRouter(prefix="/estudios", tags=["estudios"])


@router.get("/", response_model=list[EstudioOut])
async def list_estudios(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
):
    return await get_all(db, Estudio, skip=skip, limit=limit)


@router.get("/{estudio_id}", response_model=EstudioOut)
async def get_estudio(estudio_id: int, db: AsyncSession = Depends(get_db)):
    estudio = await get_by_id(db, Estudio, estudio_id)
    if not estudio:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Estudio not found")
    return estudio


@router.post("/", response_model=EstudioOut, status_code=status.HTTP_201_CREATED)
async def create_estudio(
    body: EstudioCreate,
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_user),
):
    entity = await create(db, Estudio, body.model_dump())
    await sync_all_json(db)
    return entity


@router.put("/{estudio_id}", response_model=EstudioOut)
async def update_estudio(
    estudio_id: int,
    body: EstudioUpdate,
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_user),
):
    estudio = await get_by_id(db, Estudio, estudio_id)
    if not estudio:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Estudio not found")
    entity = await update(db, estudio, body.model_dump(exclude_none=True))
    await sync_all_json(db)
    return entity


@router.delete("/{estudio_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_estudio(
    estudio_id: int,
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_user),
):
    estudio = await get_by_id(db, Estudio, estudio_id)
    if not estudio:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Estudio not found")
    await soft_delete(db, estudio)
    await sync_all_json(db)
