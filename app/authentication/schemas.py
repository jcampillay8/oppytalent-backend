# src/authentication/schemas.py
from pydantic import (
    UUID4, 
    BaseModel, 
    EmailStr, 
    Field, 
    field_validator, 
    model_validator, 
    ConfigDict
)
from typing import Optional, Dict, Any
from uuid import UUID
from app.config import settings

class AreaOperativaSimpleSchema(BaseModel):
    id: UUID
    nombre: str
    model_config = ConfigDict(from_attributes=True)

class UsuarioPublicSchema(BaseModel):
    """
    Esquema público para la información del usuario.
    Optimizado para Pydantic V2.
    """
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True
    )

    id: int
    user_guid: Optional[UUID4] = Field(None, alias="guid") 
    username: str
    email: str
    first_name: Optional[str] = Field(None, alias="firstName")
    last_name: Optional[str] = Field(None, alias="lastName")
    user_image: Optional[str] = Field(None, alias="userImage")
    occupation: Optional[str] = Field(None, alias="occupation")
    nombre_visible: Optional[str] = Field(None, alias="nombreVisible")
    phone: Optional[str] = Field(None, alias="phone")
    settings: Dict[str, Any] = Field(default_factory=dict)
    has_accepted_terms: bool = Field(..., alias="termsAccepted")
    token_expires_at: Optional[int] = Field(None, alias="tokenExpiresAt")
    role: str = "user"
    permissions: list[str] = Field(default_factory=list)
    direct_permissions: list[str] = Field(default_factory=list, alias="directPermissions")
    is_superuser: bool = Field(default=False, serialization_alias="isPropietario")
    is_impersonating: bool = Field(default=False, serialization_alias="isImpersonating")
    areas_operativas: list[AreaOperativaSimpleSchema] = Field(default_factory=list, alias="areasOperativas")

    @model_validator(mode='before')
    @classmethod
    def inject_default_tour_flag(cls, data: Any) -> Any:
        """
        Asegura que 'show_tour' exista en los settings.
        Maneja tanto diccionarios como objetos de SQLAlchemy.
        """
        # Extraer los settings actuales
        if isinstance(data, dict):
            current_settings = data.get("settings") or {}
            # Si es un dict, lo modificamos directamente
            if 'show_tour' not in current_settings:
                current_settings['show_tour'] = True
            data["settings"] = current_settings
        else:
            # Si es un objeto de SQLAlchemy (BaseModel)
            current_settings = getattr(data, "settings", {}) or {}
            if 'show_tour' not in current_settings:
                # No modificamos el objeto DB, solo los datos que van al schema
                current_settings = {**current_settings, "show_tour": True}
            
            # RBAC Permissions Calculation
            perms = set()
            direct_perms = []
            if getattr(data, "direct_permissions", None):
                direct_perms = [p.code for p in data.direct_permissions]
                perms.update(direct_perms)
            if getattr(data, "roles", None):
                for r in data.roles:
                    if getattr(r, "permissions", None):
                        perms.update(p.code for p in r.permissions)
            
            # Attaching to the object so Pydantic can read it via from_attributes
            setattr(data, "permissions", list(perms))
            setattr(data, "direct_permissions", direct_perms)
            
            return data

        return data

    @field_validator("user_image", mode="after")
    @classmethod
    def add_image_host(cls, v: Optional[str]) -> Optional[str]:
        """Añade el host de estáticos en desarrollo y preproducción."""
        if v and "/static/" in v and settings.ENVIRONMENT in ("development", "premaster"):
            static_host = str(settings.STATIC_HOST).rstrip("/")
            return f"{static_host}{v}"
        return v


class ForgotPasswordSchema(BaseModel):
    email: EmailStr = Field(..., description="Email del usuario para restablecer contraseña.")


class ResetPasswordSchema(BaseModel):
    token: str = Field(..., min_length=1)
    new_password: str = Field(..., min_length=6, max_length=128)
    confirm_password: str = Field(..., min_length=6, max_length=128)

    @model_validator(mode="after")
    def passwords_match(self) -> "ResetPasswordSchema":
        """Validador de coincidencia de contraseñas en Pydantic V2."""
        if self.new_password != self.confirm_password:
            raise ValueError("Las contraseñas no coinciden.")
        return self


class LoginResponseSchema(UsuarioPublicSchema):
    """
    Respuesta de login exitoso.
    """
    access_token: str = Field(..., alias="accessToken")
    token_type: str = Field("bearer", alias="tokenType")

class ImpersonateRequestSchema(BaseModel):
    role_id: int = Field(..., description="ID del rol a suplantar")