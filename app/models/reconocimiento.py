from sqlalchemy import String, Integer, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import BaseModel


class Reconocimiento(BaseModel):
    __tablename__ = "reconocimientos"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False, index=True)
    tipo: Mapped[str] = mapped_column(String(50), nullable=False) # PREMIO, PUBLICACION, MEDIO
    titulo: Mapped[str] = mapped_column(String(255), nullable=False)
    institucion: Mapped[str] = mapped_column(String(255), nullable=False)
    fecha: Mapped[str | None] = mapped_column(String(100), nullable=True)
    descripcion: Mapped[str] = mapped_column(Text, nullable=False)
    enlace: Mapped[str | None] = mapped_column(String(500), nullable=True)
    referencia: Mapped[str | None] = mapped_column(String(255), nullable=True)
    image_url: Mapped[str | None] = mapped_column(String(500), nullable=True)

    traducciones: Mapped[list["ReconocimientoTraduccion"]] = relationship("ReconocimientoTraduccion", back_populates="reconocimiento", cascade="all, delete-orphan", lazy="selectin")


class ReconocimientoTraduccion(BaseModel):
    __tablename__ = "reconocimiento_traducciones"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    reconocimiento_id: Mapped[int] = mapped_column(ForeignKey("reconocimientos.id", ondelete="CASCADE"), nullable=False, index=True)
    idioma: Mapped[str] = mapped_column(String(5), nullable=False, index=True)
    
    titulo: Mapped[str] = mapped_column(String(255), nullable=False)
    descripcion: Mapped[str] = mapped_column(Text, nullable=False)

    reconocimiento: Mapped["Reconocimiento"] = relationship("Reconocimiento", back_populates="traducciones")
