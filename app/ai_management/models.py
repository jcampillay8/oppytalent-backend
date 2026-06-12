# app/ai_management/models.py
from sqlalchemy import String, ForeignKey, Text, Boolean, Float, Integer
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime, timezone
from app.database import BaseModel
from app.config import settings

class LLMRequestLog(BaseModel): 
    __tablename__ = "llm_request_log" 

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    
    user_id: Mapped[int | None] = mapped_column(
        ForeignKey("usuarios.id"), 
        nullable=True
    )
    
    caller: Mapped[str] = mapped_column(String(255))
    model_name: Mapped[str] = mapped_column(String(255), nullable=False, default="unknown") 
    input_tokens: Mapped[int] = mapped_column(nullable=False, default=0)
    output_tokens: Mapped[int] = mapped_column(nullable=False, default=0)
    total_tokens: Mapped[int] = mapped_column(nullable=False, default=0)
    estimated_cost: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    
    request_duration_ms: Mapped[int | None] = mapped_column(Integer, nullable=True)
    api_success: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)

    user: Mapped["Usuario"] = relationship()


class AIModelConfig(BaseModel):
    """Configuración dinámica de modelos y precios."""
    __tablename__ = "ai_model_configs"

    id: Mapped[int] = mapped_column(primary_key=True)
    model_name: Mapped[str] = mapped_column(String(100), unique=True)
    input_price_per_million: Mapped[float] = mapped_column(Float)
    output_price_per_million: Mapped[float] = mapped_column(Float)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_default: Mapped[bool] = mapped_column(Boolean, default=False)