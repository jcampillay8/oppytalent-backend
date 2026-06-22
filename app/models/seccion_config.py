import uuid
from sqlalchemy import Uuid, String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.database import BaseModel

class SeccionConfig(BaseModel):
    __tablename__ = "seccion_configs"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4, index=True)
    usuario_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False, index=True)
    seccion: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    is_expanded: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
