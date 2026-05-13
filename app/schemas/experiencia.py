from datetime import date, datetime
from pydantic import BaseModel


class ExperienciaBase(BaseModel):
    empresa: str
    rol: str
    periodo_inicio: date
    periodo_fin: date | None = None
    descripcion_logros: str
    tags_industria: list[str] = []
    image_url: str | None = None


class ExperienciaCreate(ExperienciaBase):
    pass


class ExperienciaUpdate(BaseModel):
    empresa: str | None = None
    rol: str | None = None
    periodo_inicio: date | None = None
    periodo_fin: date | None = None
    descripcion_logros: str | None = None
    tags_industria: list[str] | None = None
    image_url: str | None = None


class ExperienciaOut(ExperienciaBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
