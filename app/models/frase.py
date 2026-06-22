import uuid
from sqlalchemy import Uuid, String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import BaseModel

class FraseCelebre(BaseModel):
    __tablename__ = "frases_celebres"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4, index=True)
    usuario_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False, index=True)
    texto: Mapped[str] = mapped_column(Text, nullable=False)
    autor: Mapped[str] = mapped_column(String(255), nullable=False)

    traducciones: Mapped[list["FraseTraduccion"]] = relationship("FraseTraduccion", back_populates="frase", cascade="all, delete-orphan", lazy="selectin")


class FraseTraduccion(BaseModel):
    __tablename__ = "frase_traducciones"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4, index=True)
    frase_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("frases_celebres.id", ondelete="CASCADE"), nullable=False, index=True)
    idioma: Mapped[str] = mapped_column(String(5), nullable=False, index=True)
    
    # Campos traducibles
    texto: Mapped[str] = mapped_column(Text, nullable=False)

    frase: Mapped["FraseCelebre"] = relationship("FraseCelebre", back_populates="traducciones")
