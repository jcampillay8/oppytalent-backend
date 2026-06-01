from datetime import date
from sqlalchemy import String, Text, Date
from sqlalchemy.types import JSON
from sqlalchemy.orm import Mapped, mapped_column

from app.database import BaseModel


class Proyecto(BaseModel):
    __tablename__ = "proyectos"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
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
