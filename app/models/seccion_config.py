from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from app.database import BaseModel

class SeccionConfig(BaseModel):
    __tablename__ = "seccion_configs"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    seccion: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    is_expanded: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
