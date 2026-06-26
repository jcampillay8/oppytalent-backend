from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime

class MessageCreate(BaseModel):
    content: str = Field(..., min_length=1)

class MessageOut(BaseModel):
    id: UUID
    conversation_id: UUID
    sender_id: UUID
    content: str
    is_read: bool
    created_at: datetime

    class Config:
        from_attributes = True

class ConversationParticipantOut(BaseModel):
    id: UUID
    username: str
    first_name: str | None = None
    last_name: str | None = None
    role: str | None = None
    userImage: str | None = None
    avatar_url: str | None = None

    class Config:
        from_attributes = True

class ConversationOut(BaseModel):
    id: UUID
    participant1_id: UUID
    participant2_id: UUID
    created_at: datetime
    updated_at: datetime
    other_participant: ConversationParticipantOut | None = None
    last_message: MessageOut | None = None
    unread_count: int = 0

    class Config:
        from_attributes = True

class ChatStartRequest(BaseModel):
    target_username: str
