from datetime import datetime
from pydantic import BaseModel


class EstudioBase(BaseModel):
    institucion: str
    titulo: str
    anio_obtencion: int
    descripcion_detallada: str
    link: str | None = None
    image_url: str | None = None


class EstudioCreate(EstudioBase):
    pass


class EstudioUpdate(BaseModel):
    institucion: str | None = None
    titulo: str | None = None
    anio_obtencion: int | None = None
    descripcion_detallada: str | None = None
    link: str | None = None
    image_url: str | None = None


class EstudioOut(EstudioBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
