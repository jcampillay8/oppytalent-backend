from datetime import date
from sqlalchemy import String, Text, Date, ForeignKey
from sqlalchemy.types import JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import BaseModel


class Experiencia(BaseModel):
    __tablename__ = "experiencias"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False, index=True)
    empresa: Mapped[str] = mapped_column(String(255), nullable=False)
    rol: Mapped[str] = mapped_column(String(255), nullable=False)
    periodo_inicio: Mapped[date] = mapped_column(Date, nullable=False)
    periodo_fin: Mapped[date | None] = mapped_column(Date, nullable=True)
    descripcion_logros: Mapped[str] = mapped_column(Text, nullable=False)
    tags_industria: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    link: Mapped[str | None] = mapped_column(String(500), nullable=True)
    link_demo: Mapped[str | None] = mapped_column(String(500), nullable=True)
    image_url: Mapped[str | None] = mapped_column(String(500), nullable=True)

    traducciones: Mapped[list["ExperienciaTraduccion"]] = relationship("ExperienciaTraduccion", back_populates="experiencia", cascade="all, delete-orphan", lazy="selectin")


class ExperienciaTraduccion(BaseModel):
    __tablename__ = "experiencia_traducciones"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    experiencia_id: Mapped[int] = mapped_column(ForeignKey("experiencias.id", ondelete="CASCADE"), nullable=False, index=True)
    idioma: Mapped[str] = mapped_column(String(5), nullable=False, index=True)
    
    # Campos traducibles
    rol: Mapped[str] = mapped_column(String(255), nullable=False)
    descripcion_logros: Mapped[str] = mapped_column(Text, nullable=False)
    tags_industria: Mapped[list] = mapped_column(JSON, nullable=False, default=list)

    experiencia: Mapped["Experiencia"] = relationship("Experiencia", back_populates="traducciones")
