from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.types import JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import BaseModel


class Perfil(BaseModel):
    __tablename__ = "perfiles"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False, index=True)
    descripcion: Mapped[str] = mapped_column(Text, nullable=False)
    image_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    avatar_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    telefono: Mapped[str | None] = mapped_column(String(50), nullable=True)
    email: Mapped[str | None] = mapped_column(String(100), nullable=True)
    linkedin: Mapped[str | None] = mapped_column(String(500), nullable=True)
    github: Mapped[str | None] = mapped_column(String(500), nullable=True)
    ciudad: Mapped[str | None] = mapped_column(String(100), nullable=True)
    youtube_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    certificaciones: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    idiomas: Mapped[list] = mapped_column(JSON, nullable=False, default=list)

    traducciones: Mapped[list["PerfilTraduccion"]] = relationship("PerfilTraduccion", back_populates="perfil", cascade="all, delete-orphan", lazy="selectin")


class PerfilTraduccion(BaseModel):
    __tablename__ = "perfil_traducciones"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    perfil_id: Mapped[int] = mapped_column(ForeignKey("perfiles.id", ondelete="CASCADE"), nullable=False, index=True)
    idioma: Mapped[str] = mapped_column(String(5), nullable=False, index=True)
    
    # Campos traducibles
    descripcion: Mapped[str] = mapped_column(Text, nullable=False)

    perfil: Mapped["Perfil"] = relationship("Perfil", back_populates="traducciones")
