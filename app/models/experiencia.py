from datetime import date
from sqlalchemy import String, Text, Date
from sqlalchemy.types import JSON
from sqlalchemy.orm import Mapped, mapped_column

from app.database import BaseModel


class Experiencia(BaseModel):
    __tablename__ = "experiencias"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    empresa: Mapped[str] = mapped_column(String(255), nullable=False)
    rol: Mapped[str] = mapped_column(String(255), nullable=False)
    periodo_inicio: Mapped[date] = mapped_column(Date, nullable=False)
    periodo_fin: Mapped[date | None] = mapped_column(Date, nullable=True)
    descripcion_logros: Mapped[str] = mapped_column(Text, nullable=False)
    tags_industria: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
