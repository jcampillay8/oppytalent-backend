from pydantic import BaseModel
from datetime import datetime


class HabilitacionTraduccionBase(BaseModel):
    idioma: str
    titulo: str
    descripcion: str

class HabilitacionTraduccionCreate(HabilitacionTraduccionBase):
    pass

class HabilitacionTraduccionOut(HabilitacionTraduccionBase):
    id: int
    habilitacion_id: int

    model_config = {"from_attributes": True}

class HabilitacionBase(BaseModel):
    tipo: str
    titulo: str
    descripcion: str

class HabilitacionCreate(HabilitacionBase):
    traducciones: list[HabilitacionTraduccionCreate] = []

class HabilitacionUpdate(BaseModel):
    tipo: str | None = None
    titulo: str | None = None
    descripcion: str | None = None
    traducciones: list[HabilitacionTraduccionCreate] | None = None

class HabilitacionOut(HabilitacionBase):
    id: int
    usuario_id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    traducciones: list[HabilitacionTraduccionOut] = []

    model_config = {"from_attributes": True}
