from datetime import datetime
from sqlalchemy import Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.database import Base

class CoverLetter(Base):
    __tablename__ = "cover_letters"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    usuario_id: Mapped[int] = mapped_column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False)
    
    # Datos de la oferta de trabajo
    job_title: Mapped[str] = mapped_column(String(255), nullable=False)
    company_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    job_description: Mapped[str] = mapped_column(Text, nullable=False)
    
    # La carta generada
    generated_letter: Mapped[str] = mapped_column(Text, nullable=False)
    
    # Si la generó el reclutador o el propio talento
    generated_by: Mapped[str] = mapped_column(String(50), default="visitor") # 'visitor' or 'owner'
    
    # Datos de contacto del reclutador (opcional, para capturar leads)
    recruiter_email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    
    usuario: Mapped["Usuario"] = relationship("Usuario", back_populates="cover_letters")
