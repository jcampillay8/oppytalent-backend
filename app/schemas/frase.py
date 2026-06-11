from pydantic import BaseModel, ConfigDict

class FraseTraduccionBase(BaseModel):
    idioma: str
    texto: str

class FraseTraduccionCreate(FraseTraduccionBase):
    pass

class FraseTraduccionOut(FraseTraduccionBase):
    id: int
    frase_id: int

    model_config = ConfigDict(from_attributes=True)

class FraseCelebreBase(BaseModel):
    texto: str
    autor: str

class FraseCelebreCreate(FraseCelebreBase):
    traducciones: list[FraseTraduccionCreate] = []

class FraseCelebreUpdate(BaseModel):
    texto: str | None = None
    autor: str | None = None
    traducciones: list[FraseTraduccionCreate] | None = None

class FraseCelebreResponse(FraseCelebreBase):
    id: int
    traducciones: list[FraseTraduccionOut] = []

    model_config = ConfigDict(from_attributes=True)
