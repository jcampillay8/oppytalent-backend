from pydantic import BaseModel, ConfigDict

class FraseCelebreBase(BaseModel):
    texto: str
    autor: str

class FraseCelebreCreate(FraseCelebreBase):
    pass

class FraseCelebreUpdate(FraseCelebreBase):
    pass

class FraseCelebreResponse(FraseCelebreBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
