import uuid
from sqlalchemy import Uuid, String, Text, Boolean, DateTime, Integer, JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from app.authentication.models import UsuarioSessionHistory, PasswordResetToken, RefreshToken, EmailConfirmationToken

from app.database import BaseModel


class Usuario(BaseModel):
    __tablename__ = "usuarios"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4, index=True)
    username: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(Text, nullable=False)
    role: Mapped[str] = mapped_column(String(20), default="VIEWER", nullable=False) # Legacy role
    
    # RBAC Support
    role_id: Mapped[uuid.UUID | None] = mapped_column(Uuid, ForeignKey("roles.id"), nullable=True)
    rbac_role = relationship("Role")
    
    first_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    last_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    user_image: Mapped[str | None] = mapped_column(String(1048), nullable=True)
    custom_slug: Mapped[str | None] = mapped_column(String(100), unique=True, nullable=True, index=True)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    has_accepted_terms: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    
    # B2B Ecosystem Fields
    is_recruiter: Mapped[bool] = mapped_column(Boolean, default=False, server_default="false", nullable=False)
    is_visible_b2b: Mapped[bool] = mapped_column(Boolean, default=False, server_default="false", nullable=False)
    
    chat_welcome_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    ai_pitch_rules: Mapped[list] = mapped_column(JSON, default=list, server_default='[]', nullable=False)
    portfolio_theme: Mapped[str | None] = mapped_column(String(50), default="dark-glass", nullable=True)
    portfolio_layout: Mapped[str | None] = mapped_column(String(20), default="tabs", server_default="tabs", nullable=True)
    
    # Premium & Integrations
    is_premium: Mapped[bool] = mapped_column(Boolean, default=False, server_default="false", nullable=False)
    google_access_token: Mapped[str | None] = mapped_column(String(2048), nullable=True)
    google_refresh_token: Mapped[str | None] = mapped_column(String(2048), nullable=True)
    google_token_expiry: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    
    # AI Config
    encrypted_gemini_key: Mapped[str | None] = mapped_column(String(2048), nullable=True)
    ai_credits: Mapped[int] = mapped_column(Integer, default=50, server_default="50", nullable=False)
    
    # Storage
    storage_used: Mapped[int] = mapped_column(Integer, default=0, server_default="0", nullable=False)
    
    last_login: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    failed_login_attempts: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    locked_until: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    
    session_history: Mapped[List["UsuarioSessionHistory"]] = relationship("UsuarioSessionHistory", back_populates="user")
    password_reset_tokens: Mapped[List["PasswordResetToken"]] = relationship("PasswordResetToken", back_populates="user")
    refresh_tokens: Mapped[List["RefreshToken"]] = relationship("RefreshToken", back_populates="user")
    email_confirmation_tokens: Mapped[List["EmailConfirmationToken"]] = relationship("EmailConfirmationToken", back_populates="user")
    
