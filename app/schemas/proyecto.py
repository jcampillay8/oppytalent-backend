from datetime import date, datetime
from pydantic import BaseModel


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


class ProyectoCreate(ProyectoBase):
    pass


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


class ProyectoOut(ProyectoBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
