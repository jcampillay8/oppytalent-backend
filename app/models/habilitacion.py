import uuid
from sqlalchemy import Uuid, String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import BaseModel


class Habilitacion(BaseModel):
    __tablename__ = "habilitaciones"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4, index=True)
    usuario_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False, index=True)
    tipo: Mapped[str] = mapped_column(String(50), nullable=False) # DISPONIBILIDAD, LICENCIA
    titulo: Mapped[str] = mapped_column(String(255), nullable=False)
    descripcion: Mapped[str] = mapped_column(Text, nullable=False)
    image_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    enlace: Mapped[str | None] = mapped_column(String(500), nullable=True)

    traducciones: Mapped[list["HabilitacionTraduccion"]] = relationship("HabilitacionTraduccion", back_populates="habilitacion", cascade="all, delete-orphan", lazy="selectin")


class HabilitacionTraduccion(BaseModel):
    __tablename__ = "habilitacion_traducciones"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4, index=True)
    habilitacion_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("habilitaciones.id", ondelete="CASCADE"), nullable=False, index=True)
    idioma: Mapped[str] = mapped_column(String(5), nullable=False, index=True)
    
    titulo: Mapped[str] = mapped_column(String(255), nullable=False)
    descripcion: Mapped[str] = mapped_column(Text, nullable=False)

    habilitacion: Mapped["Habilitacion"] = relationship("Habilitacion", back_populates="traducciones")
