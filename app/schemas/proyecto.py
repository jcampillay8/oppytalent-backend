from datetime import date, datetime
from pydantic import BaseModel


class ProyectoTraduccionBase(BaseModel):
    idioma: str
    titulo: str
    descripcion_corta: str
    descripcion_detallada: str
    stack_tecnologico: list[str] = []
    kpis: dict | None = None
    tags: list[str] = []

class ProyectoTraduccionCreate(ProyectoTraduccionBase):
    pass

class ProyectoTraduccionOut(ProyectoTraduccionBase):
    id: int
    proyecto_id: int

    model_config = {"from_attributes": True}

class ProyectoBase(BaseModel):
    titulo: str
    descripcion_corta: str
    descripcion_detallada: str
    stack_tecnologico: list[str] = []
    fecha_proyecto: date
    link_github: str | None = None
    link_demo: str | None = None
    kpis: dict | None = None
    tags: list[str] = []
    image_url: str | None = None
    youtube_url: str | None = None


class ProyectoCreate(ProyectoBase):
    traducciones: list[ProyectoTraduccionCreate] = []


class ProyectoUpdate(BaseModel):
    titulo: str | None = None
    descripcion_corta: str | None = None
    descripcion_detallada: str | None = None
    stack_tecnologico: list[str] | None = None
    fecha_proyecto: date | None = None
    link_github: str | None = None
    link_demo: str | None = None
    kpis: dict | None = None
    tags: list[str] | None = None
    image_url: str | None = None
    youtube_url: str | None = None
    traducciones: list[ProyectoTraduccionCreate] | None = None


class ProyectoOut(ProyectoBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    traducciones: list[ProyectoTraduccionOut] = []

    model_config = {"from_attributes": True}
