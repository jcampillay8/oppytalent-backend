# src/registration/schemas.py

from pydantic import BaseModel, EmailStr, Field

class UsuarioRegisterSchema(BaseModel):
    email: EmailStr
    username: str = Field(max_length=150)
    password: str = Field(min_length=6, max_length=128)
    first_name: str = Field(max_length=150)
    last_name: str = Field(max_length=150)
    terms_accepted: bool = Field(..., description="Usuario's acceptance of terms and conditions")
    referral_code: str | None = Field(default=None, max_length=100)