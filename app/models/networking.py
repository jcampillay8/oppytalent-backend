import uuid
import enum
from sqlalchemy import Uuid, String, Enum, Float, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from app.database import BaseModel
from datetime import datetime

class ConnectionStatus(str, enum.Enum):
    PENDING = "PENDING"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"
    BLOCKED = "BLOCKED"

class NetworkConnection(BaseModel):
    __tablename__ = "network_connections"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4, index=True)
    requester_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False, index=True)
    addressee_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False, index=True)
    status: Mapped[ConnectionStatus] = mapped_column(Enum(ConnectionStatus), default=ConnectionStatus.PENDING, nullable=False, index=True)
    affinity_score: Mapped[float] = mapped_column(Float, default=0.1, server_default="0.1", nullable=False)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    requester = relationship("Usuario", foreign_keys=[requester_id])
    addressee = relationship("Usuario", foreign_keys=[addressee_id])


class NetworkFollow(BaseModel):
    __tablename__ = "network_follows"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4, index=True)
    follower_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False, index=True)
    following_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False, index=True)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    follower = relationship("Usuario", foreign_keys=[follower_id])
    following = relationship("Usuario", foreign_keys=[following_id])


class FeedEventType(str, enum.Enum):
    NEW_PROJECT = "NEW_PROJECT"
    NEW_EXPERIENCE = "NEW_EXPERIENCE"
    NEW_CERTIFICATION = "NEW_CERTIFICATION"
    NEW_STUDY = "NEW_STUDY"

class FeedEvent(BaseModel):
    __tablename__ = "feed_events"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4, index=True)
    user_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False, index=True)
    event_type: Mapped[FeedEventType] = mapped_column(Enum(FeedEventType), nullable=False)
    entity_id: Mapped[uuid.UUID] = mapped_column(Uuid, nullable=False) # ID of the project/experience
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    user = relationship("Usuario", foreign_keys=[user_id])


class NetworkSuggestion(BaseModel):
    __tablename__ = "network_suggestions"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4, index=True)
    user_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False, index=True)
    suggested_user_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False, index=True)
    reason: Mapped[str] = mapped_column(String, nullable=False)
    affinity_score: Mapped[float] = mapped_column(Float, default=0.5, server_default="0.5", nullable=False)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    user = relationship("Usuario", foreign_keys=[user_id])
    suggested_user = relationship("Usuario", foreign_keys=[suggested_user_id])
