from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.database import BaseModel


class Estudio(BaseModel):
    __tablename__ = "estudios"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    institucion: Mapped[str] = mapped_column(String(255), nullable=False)
    titulo: Mapped[str] = mapped_column(String(255), nullable=False)
    anio_obtencion: Mapped[int] = mapped_column(Integer, nullable=False)
    image_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
