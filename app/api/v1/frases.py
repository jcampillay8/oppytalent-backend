from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_admin_user
from app.models.frase import FraseCelebre
from app.schemas.frase import FraseCelebreCreate, FraseCelebreResponse, FraseCelebreUpdate
from app.services.crud import get_all, get_by_id, create, update, soft_delete

router = APIRouter(prefix="/frases", tags=["frases"])


@router.get("/", response_model=list[FraseCelebreResponse])
async def list_frases(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
):
    return await get_all(db, FraseCelebre, skip=skip, limit=limit)


@router.get("/{frase_id}", response_model=FraseCelebreResponse)
async def get_frase(frase_id: int, db: AsyncSession = Depends(get_db)):
    frase = await get_by_id(db, FraseCelebre, frase_id)
    if not frase:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Frase not found")
    return frase


@router.post("/", response_model=FraseCelebreResponse, status_code=status.HTTP_201_CREATED)
async def create_frase(
    body: FraseCelebreCreate,
    db: AsyncSession = Depends(get_db),
    _=Depends(get_admin_user),
):
    entity = await create(db, FraseCelebre, body.model_dump())
    return entity


@router.put("/{frase_id}", response_model=FraseCelebreResponse)
async def update_frase(
    frase_id: int,
    body: FraseCelebreUpdate,
    db: AsyncSession = Depends(get_db),
    _=Depends(get_admin_user),
):
    frase = await get_by_id(db, FraseCelebre, frase_id)
    if not frase:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Frase not found")
    entity = await update(db, frase, body.model_dump(exclude_none=True))
    return entity


@router.delete("/{frase_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_frase(
    frase_id: int,
    db: AsyncSession = Depends(get_db),
    _=Depends(get_admin_user),
):
    frase = await get_by_id(db, FraseCelebre, frase_id)
    if not frase:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Frase not found")
    await soft_delete(db, frase)
