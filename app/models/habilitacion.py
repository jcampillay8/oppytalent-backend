from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import BaseModel


class Habilitacion(BaseModel):
    __tablename__ = "habilitaciones"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False, index=True)
    tipo: Mapped[str] = mapped_column(String(50), nullable=False) # DISPONIBILIDAD, LICENCIA
    titulo: Mapped[str] = mapped_column(String(255), nullable=False)
    descripcion: Mapped[str] = mapped_column(Text, nullable=False)

    traducciones: Mapped[list["HabilitacionTraduccion"]] = relationship("HabilitacionTraduccion", back_populates="habilitacion", cascade="all, delete-orphan", lazy="selectin")


class HabilitacionTraduccion(BaseModel):
    __tablename__ = "habilitacion_traducciones"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    habilitacion_id: Mapped[int] = mapped_column(ForeignKey("habilitaciones.id", ondelete="CASCADE"), nullable=False, index=True)
    idioma: Mapped[str] = mapped_column(String(5), nullable=False, index=True)
    
    titulo: Mapped[str] = mapped_column(String(255), nullable=False)
    descripcion: Mapped[str] = mapped_column(Text, nullable=False)

    habilitacion: Mapped["Habilitacion"] = relationship("Habilitacion", back_populates="traducciones")
