# # src/authentication/models.py
import uuid
from datetime import datetime, timezone
from typing import TYPE_CHECKING, List

from sqlalchemy import Uuid, Boolean, DateTime, ForeignKey, Index, String, func, Integer, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.config import settings
from app.database import BaseModel

if TYPE_CHECKING:
    from app.models import Usuario

# --- Historial de Sesiones ---
class UsuarioSessionHistory(BaseModel):
    __tablename__ = "user_session_history"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("usuarios.id", ondelete="CASCADE"))
    login_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())
    logout_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    ip_address: Mapped[str] = mapped_column(String(45), nullable=True)
    user_agent: Mapped[str] = mapped_column(String(500), nullable=True)
    
    user: Mapped["Usuario"] = relationship("Usuario", back_populates="session_history")

    __table_args__ = (
        Index("idx_session_user_id", "user_id"),
        Index("idx_session_login_time", "login_time"),
    )

# --- Token de Restablecimiento de Contraseña ---
class PasswordResetToken(BaseModel):
    __tablename__ = "password_reset_tokens"
    
    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("usuarios.id", ondelete="CASCADE"))
    token: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    is_used: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    
    user: Mapped["Usuario"] = relationship("Usuario", back_populates="password_reset_tokens")

    __table_args__ = (
        Index("idx_reset_token_user_id", "user_id"),
        Index("idx_reset_token_token", "token"),
        Index("idx_reset_token_expires_at", "expires_at"),
    )

# --- Refresh Token ---
class RefreshToken(BaseModel):
    __tablename__ = "refresh_tokens"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("usuarios.id", ondelete="CASCADE"))
    token: Mapped[str] = mapped_column(String(500), unique=True, nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    is_revoked: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    ip_address: Mapped[str] = mapped_column(String(45), nullable=True)
    user_agent: Mapped[str] = mapped_column(String(500), nullable=True)
    
    user: Mapped["Usuario"] = relationship("Usuario", back_populates="refresh_tokens")

    __table_args__ = (
        Index("idx_refresh_token_user_id", "user_id"),
        Index("idx_refresh_token_token", "token"),
        Index("idx_refresh_token_expires_at", "expires_at"),
    )

# --- Token de Confirmación de Correo Electrónico ---
class EmailConfirmationToken(BaseModel):
    __tablename__ = "email_confirmation_tokens"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    user_email: Mapped[str] = mapped_column(String(255), nullable=False)
    token: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    user_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("usuarios.id", ondelete="SET NULL"), nullable=True)
    username: Mapped[str] = mapped_column(String(255), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    first_name: Mapped[str] = mapped_column(String(255), nullable=True)
    last_name: Mapped[str] = mapped_column(String(255), nullable=True)
    terms_accepted: Mapped[bool] = mapped_column(Boolean, nullable=False)
    image_url: Mapped[str] = mapped_column(String(1048), nullable=True)
    referral_code: Mapped[str | None] = mapped_column(String(100), nullable=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    is_used: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    
    user: Mapped["Usuario"] = relationship("Usuario", back_populates="email_confirmation_tokens")

    __table_args__ = (
        Index("idx_email_confirmation_token_token", "token"),
    )