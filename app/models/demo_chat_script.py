import uuid
from sqlalchemy import Uuid, String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import BaseModel

class DemoChatScript(BaseModel):
    __tablename__ = "demo_chat_scripts"

    usuario_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("usuarios.id", ondelete="CASCADE"), primary_key=True)
    step_1: Mapped[str] = mapped_column(Text, nullable=False)
    step_2: Mapped[str] = mapped_column(Text, nullable=False)
    step_3: Mapped[str] = mapped_column(Text, nullable=False)
