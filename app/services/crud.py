from typing import Any, Sequence

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import BaseModel
from app.services.image import parse_image_url


async def get_all(
    db: AsyncSession,
    model: type[BaseModel],
    skip: int = 0,
    limit: int = 100,
    filters: dict[str, Any] | None = None,
    order_by: Any | None = None,
) -> Sequence[BaseModel]:
    query = select(model).where(model.is_active == True)

    if filters:
        for field, value in filters.items():
            if hasattr(model, field) and value is not None:
                column = getattr(model, field)
                if isinstance(value, list):
                    query = query.where(column.in_(value))
                else:
                    query = query.where(column == value)

    if order_by is not None:
        query = query.order_by(order_by)
    else:
        query = query.order_by(model.updated_at.desc())

    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


async def get_by_id(db: AsyncSession, model: type[BaseModel], entity_id: int) -> BaseModel | None:
    result = await db.execute(
        select(model).where(model.id == entity_id, model.is_active == True)
    )
    return result.scalar_one_or_none()


async def create(db: AsyncSession, model: type[BaseModel], data: dict) -> BaseModel:
    for key in ("image_url", "avatar_url"):
        if key in data:
            data[key] = parse_image_url(data.get(key))
    entity = model(**data)
    db.add(entity)
    await db.flush()
    await db.refresh(entity)
    return entity


async def update(db: AsyncSession, entity: BaseModel, data: dict) -> BaseModel:
    for key in ("image_url", "avatar_url"):
        if key in data:
            data[key] = parse_image_url(data.get(key))
    for field, value in data.items():
        if value is not None:
            setattr(entity, field, value)
    await db.flush()
    await db.refresh(entity)
    return entity


async def soft_delete(db: AsyncSession, entity: BaseModel) -> None:
    entity.is_active = False
    await db.flush()
