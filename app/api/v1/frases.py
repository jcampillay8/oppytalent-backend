from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_user
from app.models.frase import FraseCelebre
from app.schemas.frase import FraseCelebreCreate, FraseCelebreResponse, FraseCelebreUpdate
from app.services.crud import get_all, get_by_id, create, update, soft_delete

router = APIRouter(prefix="/frases", tags=["frases"])


@router.get("/", response_model=list[FraseCelebreResponse])
async def list_frases(
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
    return await get_all(db, FraseCelebre, skip=skip, limit=limit, filters=filters)


@router.get("/{frase_id}", response_model=FraseCelebreResponse)
async def get_frase(frase_id: UUID, db: AsyncSession = Depends(get_db)):
    frase = await get_by_id(db, FraseCelebre, frase_id)
    if not frase:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Frase not found")
    return frase


@router.post("/", response_model=FraseCelebreResponse, status_code=status.HTTP_201_CREATED)
async def create_frase(
    body: FraseCelebreCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    data = body.model_dump()
    data["usuario_id"] = current_user.id
    entity = await create(db, FraseCelebre, data)
    return entity


@router.put("/{frase_id}", response_model=FraseCelebreResponse)
async def update_frase(
    frase_id: UUID,
    body: FraseCelebreUpdate,
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_user),
):
    frase = await get_by_id(db, FraseCelebre, frase_id)
    if not frase:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Frase not found")
    entity = await update(db, frase, body.model_dump(exclude_none=True))
    return entity


@router.delete("/{frase_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_frase(
    frase_id: UUID,
    db: AsyncSession = Depends(get_db),
    _=Depends(get_current_user),
):
    frase = await get_by_id(db, FraseCelebre, frase_id)
    if not frase:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Frase not found")
    await soft_delete(db, frase)
