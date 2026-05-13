from datetime import datetime
from pydantic import BaseModel


class PerfilBase(BaseModel):
    descripcion: str
    image_url: str | None = None
    avatar_url: str | None = None


class PerfilCreate(PerfilBase):
    pass


class PerfilUpdate(BaseModel):
    descripcion: str | None = None
    image_url: str | None = None
    avatar_url: str | None = None


class PerfilOut(PerfilBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
