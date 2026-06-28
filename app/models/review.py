from uuid import UUID
import uuid
from sqlalchemy import String, Integer, Text, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

from app.database import BaseModel

class Review(BaseModel):
    __tablename__ = "reviews"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    usuario_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False, unique=True)
    rating: Mapped[int] = mapped_column(Integer, default=5, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    
    # We can store a denormalized count for performance
    likes_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    
    author = relationship("Usuario")
    likes = relationship("ReviewLike", back_populates="review", cascade="all, delete-orphan")

class ReviewLike(BaseModel):
    __tablename__ = "review_likes"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, index=True)
    review_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("reviews.id", ondelete="CASCADE"), nullable=False, index=True)
    usuario_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    
    review = relationship("Review", back_populates="likes")
