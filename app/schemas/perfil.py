from datetime import datetime
from pydantic import BaseModel


class PerfilTraduccionBase(BaseModel):
    idioma: str
    descripcion: str

class PerfilTraduccionCreate(PerfilTraduccionBase):
    pass

class PerfilTraduccionOut(PerfilTraduccionBase):
    id: int
    perfil_id: int

    model_config = {"from_attributes": True}

class PerfilBase(BaseModel):
    nombre_completo: str | None = None
    ocupacion: str | None = None
    descripcion: str
    image_url: str | None = None
    avatar_url: str | None = None
    telefono: str | None = None
    email: str | None = None
    linkedin: str | None = None
    github: str | None = None
    ciudad: str | None = None
    youtube_url: str | None = None
    certificaciones: list[dict] = []
    idiomas: list[dict] = []


class PerfilCreate(PerfilBase):
    traducciones: list[PerfilTraduccionCreate] = []


class PerfilUpdate(BaseModel):
    nombre_completo: str | None = None
    ocupacion: str | None = None
    descripcion: str | None = None
    image_url: str | None = None
    avatar_url: str | None = None
    telefono: str | None = None
    email: str | None = None
    linkedin: str | None = None
    github: str | None = None
    ciudad: str | None = None
    youtube_url: str | None = None
    certificaciones: list[dict] | None = None
    idiomas: list[dict] | None = None
    traducciones: list[PerfilTraduccionCreate] | None = None


class PerfilOut(PerfilBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    traducciones: list[PerfilTraduccionOut] = []

    model_config = {"from_attributes": True}
