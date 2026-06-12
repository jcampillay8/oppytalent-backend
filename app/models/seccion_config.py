from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.database import BaseModel

class SeccionConfig(BaseModel):
    __tablename__ = "seccion_configs"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False, index=True)
    seccion: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    is_expanded: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
