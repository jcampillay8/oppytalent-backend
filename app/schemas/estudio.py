from uuid import UUID
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel


class EstudioTraduccionBase(BaseModel):
    idioma: str
    titulo: str
    descripcion_detallada: str

class EstudioTraduccionCreate(EstudioTraduccionBase):
    pass

class EstudioTraduccionOut(EstudioTraduccionBase):
    id: UUID
    estudio_id: UUID

    model_config = {"from_attributes": True}

class EstudioBase(BaseModel):
    institucion: str
    titulo: str
    anio_obtencion: int
    descripcion_detallada: str
    link: str | None = None
    image_url: str | None = None


class EstudioCreate(EstudioBase):
    traducciones: list[EstudioTraduccionCreate] = []


class EstudioUpdate(BaseModel):
    institucion: str | None = None
    titulo: str | None = None
    anio_obtencion: int | None = None
    descripcion_detallada: str | None = None
    link: str | None = None
    image_url: str | None = None
    traducciones: list[EstudioTraduccionCreate] | None = None


class EstudioOut(EstudioBase):
    id: UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime
    traducciones: list[EstudioTraduccionOut] = []

    model_config = {"from_attributes": True}
