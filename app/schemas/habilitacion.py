from uuid import UUID
from uuid import UUID
from pydantic import BaseModel
from datetime import datetime


class HabilitacionTraduccionBase(BaseModel):
    idioma: str
    titulo: str
    descripcion: str

class HabilitacionTraduccionCreate(HabilitacionTraduccionBase):
    pass

class HabilitacionTraduccionOut(HabilitacionTraduccionBase):
    id: UUID
    habilitacion_id: UUID

    model_config = {"from_attributes": True}

class HabilitacionBase(BaseModel):
    tipo: str
    titulo: str
    descripcion: str
    image_url: str | None = None
    enlace: str | None = None

class HabilitacionCreate(HabilitacionBase):
    traducciones: list[HabilitacionTraduccionCreate] = []

class HabilitacionUpdate(BaseModel):
    tipo: str | None = None
    titulo: str | None = None
    descripcion: str | None = None
    image_url: str | None = None
    enlace: str | None = None
    traducciones: list[HabilitacionTraduccionCreate] | None = None

class HabilitacionOut(HabilitacionBase):
    id: UUID
    usuario_id: UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime
    traducciones: list[HabilitacionTraduccionOut] = []

    model_config = {"from_attributes": True}
