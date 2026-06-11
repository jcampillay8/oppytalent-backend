from sqlalchemy import String, Integer, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import BaseModel


class Estudio(BaseModel):
    __tablename__ = "estudios"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    institucion: Mapped[str] = mapped_column(String(255), nullable=False)
    titulo: Mapped[str] = mapped_column(String(255), nullable=False)
    anio_obtencion: Mapped[int] = mapped_column(Integer, nullable=False)
    descripcion_detallada: Mapped[str] = mapped_column(Text, nullable=False)
    link: Mapped[str | None] = mapped_column(String(500), nullable=True)
    image_url: Mapped[str | None] = mapped_column(String(500), nullable=True)

    traducciones: Mapped[list["EstudioTraduccion"]] = relationship("EstudioTraduccion", back_populates="estudio", cascade="all, delete-orphan", lazy="selectin")


class EstudioTraduccion(BaseModel):
    __tablename__ = "estudio_traducciones"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    estudio_id: Mapped[int] = mapped_column(ForeignKey("estudios.id", ondelete="CASCADE"), nullable=False, index=True)
    idioma: Mapped[str] = mapped_column(String(5), nullable=False, index=True)
    
    # Campos traducibles
    titulo: Mapped[str] = mapped_column(String(255), nullable=False)
    descripcion_detallada: Mapped[str] = mapped_column(Text, nullable=False)

    estudio: Mapped["Estudio"] = relationship("Estudio", back_populates="traducciones")
