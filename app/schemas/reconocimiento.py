from pydantic import BaseModel
from datetime import datetime


class ReconocimientoTraduccionBase(BaseModel):
    idioma: str
    titulo: str
    descripcion: str

class ReconocimientoTraduccionCreate(ReconocimientoTraduccionBase):
    pass

class ReconocimientoTraduccionOut(ReconocimientoTraduccionBase):
    id: int
    reconocimiento_id: int

    model_config = {"from_attributes": True}

class ReconocimientoBase(BaseModel):
    tipo: str
    titulo: str
    institucion: str
    fecha: str | None = None
    descripcion: str
    enlace: str | None = None
    referencia: str | None = None
    image_url: str | None = None

class ReconocimientoCreate(ReconocimientoBase):
    traducciones: list[ReconocimientoTraduccionCreate] = []

class ReconocimientoUpdate(BaseModel):
    tipo: str | None = None
    titulo: str | None = None
    institucion: str | None = None
    fecha: str | None = None
    descripcion: str | None = None
    enlace: str | None = None
    referencia: str | None = None
    image_url: str | None = None
    traducciones: list[ReconocimientoTraduccionCreate] | None = None

class ReconocimientoOut(ReconocimientoBase):
    id: int
    usuario_id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    traducciones: list[ReconocimientoTraduccionOut] = []

    model_config = {"from_attributes": True}
