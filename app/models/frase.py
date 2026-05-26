from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.database import BaseModel

class FraseCelebre(BaseModel):
    __tablename__ = "frases_celebres"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    texto: Mapped[str] = mapped_column(Text, nullable=False)
    autor: Mapped[str] = mapped_column(String(255), nullable=False)
