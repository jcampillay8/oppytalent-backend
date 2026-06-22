import uuid
from datetime import date
from sqlalchemy import Uuid, String, Text, Date, ForeignKey
from sqlalchemy.types import JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import BaseModel


class Proyecto(BaseModel):
    __tablename__ = "proyectos"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4, index=True)
    usuario_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False, index=True)
    titulo: Mapped[str] = mapped_column(String(255), nullable=False)
    descripcion_corta: Mapped[str] = mapped_column(Text, nullable=False)
    descripcion_detallada: Mapped[str] = mapped_column(Text, nullable=False)
    stack_tecnologico: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    fecha_proyecto: Mapped[date] = mapped_column(Date, nullable=False)
    link_github: Mapped[str | None] = mapped_column(String(500), nullable=True)
    link_demo: Mapped[str | None] = mapped_column(String(500), nullable=True)
    kpis: Mapped[dict | None] = mapped_column(JSON, nullable=True, default=dict)
    tags: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    image_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    youtube_url: Mapped[str | None] = mapped_column(String(500), nullable=True)

    traducciones: Mapped[list["ProyectoTraduccion"]] = relationship("ProyectoTraduccion", back_populates="proyecto", cascade="all, delete-orphan", lazy="selectin")


class ProyectoTraduccion(BaseModel):
    __tablename__ = "proyecto_traducciones"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4, index=True)
    proyecto_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("proyectos.id", ondelete="CASCADE"), nullable=False, index=True)
    idioma: Mapped[str] = mapped_column(String(5), nullable=False, index=True) # ej: 'en', 'es'
    
    # Campos traducibles
    titulo: Mapped[str] = mapped_column(String(255), nullable=False)
    descripcion_corta: Mapped[str] = mapped_column(Text, nullable=False)
    descripcion_detallada: Mapped[str] = mapped_column(Text, nullable=False)
    stack_tecnologico: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    kpis: Mapped[dict | None] = mapped_column(JSON, nullable=True, default=dict)
    tags: Mapped[list] = mapped_column(JSON, nullable=False, default=list)

    proyecto: Mapped["Proyecto"] = relationship("Proyecto", back_populates="traducciones")
