from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import BaseModel


class Perfil(BaseModel):
    __tablename__ = "perfiles"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    descripcion: Mapped[str] = mapped_column(Text, nullable=False)
    image_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    avatar_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    telefono: Mapped[str | None] = mapped_column(String(50), nullable=True)
    email: Mapped[str | None] = mapped_column(String(100), nullable=True)
    linkedin: Mapped[str | None] = mapped_column(String(500), nullable=True)
    github: Mapped[str | None] = mapped_column(String(500), nullable=True)
    ciudad: Mapped[str | None] = mapped_column(String(100), nullable=True)
