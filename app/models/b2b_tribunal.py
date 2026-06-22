import uuid
from typing import Optional, List
from sqlalchemy import Uuid, String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import BaseModel

class TribunalLog(BaseModel):
    __tablename__ = "b2b_tribunal_logs"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4, index=True)
    recruiter_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("usuarios.id", ondelete="CASCADE"), index=True)
    question: Mapped[str] = mapped_column(Text, nullable=False)
    moderator_summary: Mapped[str] = mapped_column(Text, nullable=False)

    # Relaciones
    recruiter: Mapped["Usuario"] = relationship(foreign_keys=[recruiter_id])
    participants: Mapped[List["TribunalParticipant"]] = relationship("TribunalParticipant", back_populates="tribunal_log", cascade="all, delete-orphan")

class TribunalParticipant(BaseModel):
    __tablename__ = "b2b_tribunal_participants"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4, index=True)
    tribunal_log_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("b2b_tribunal_logs.id", ondelete="CASCADE"), index=True)
    candidate_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("usuarios.id", ondelete="CASCADE"), index=True)
    clone_answer: Mapped[str] = mapped_column(Text, nullable=False)
    
    # Optional AI-generated feedback specifically for the talent
    talent_feedback: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Relaciones
    tribunal_log: Mapped["TribunalLog"] = relationship("TribunalLog", back_populates="participants")
    candidate: Mapped["Usuario"] = relationship(foreign_keys=[candidate_id])
