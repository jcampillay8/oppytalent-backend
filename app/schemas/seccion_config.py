from pydantic import BaseModel

class SeccionConfigBase(BaseModel):
    seccion: str
    is_expanded: bool

class SeccionConfigCreate(SeccionConfigBase):
    pass

class SeccionConfigUpdate(BaseModel):
    is_expanded: bool

class SeccionConfigResponse(SeccionConfigBase):
    id: int

    class Config:
        from_attributes = True
