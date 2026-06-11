from datetime import date, datetime
from pydantic import BaseModel


class ExperienciaTraduccionBase(BaseModel):
    idioma: str
    rol: str
    descripcion_logros: str
    tags_industria: list[str] = []

class ExperienciaTraduccionCreate(ExperienciaTraduccionBase):
    pass

class ExperienciaTraduccionOut(ExperienciaTraduccionBase):
    id: int
    experiencia_id: int

    model_config = {"from_attributes": True}

class ExperienciaBase(BaseModel):
    empresa: str
    rol: str
    periodo_inicio: date
    periodo_fin: date | None = None
    descripcion_logros: str
    tags_industria: list[str] = []
    link: str | None = None
    link_demo: str | None = None
    image_url: str | None = None


class ExperienciaCreate(ExperienciaBase):
    traducciones: list[ExperienciaTraduccionCreate] = []


class ExperienciaUpdate(BaseModel):
    empresa: str | None = None
    rol: str | None = None
    periodo_inicio: date | None = None
    periodo_fin: date | None = None
    descripcion_logros: str | None = None
    tags_industria: list[str] | None = None
    link: str | None = None
    link_demo: str | None = None
    image_url: str | None = None
    traducciones: list[ExperienciaTraduccionCreate] | None = None


class ExperienciaOut(ExperienciaBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    traducciones: list[ExperienciaTraduccionOut] = []

    model_config = {"from_attributes": True}
