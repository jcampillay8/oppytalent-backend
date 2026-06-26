from fastapi import APIRouter, Depends, HTTPException, status, WebSocket, WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, and_, update, func
from typing import List
from uuid import UUID
from jose import JWTError, jwt

from app.config import settings
from app.database import get_db
from app.dependencies import get_current_user
from app.models.usuario import Usuario
from app.models.perfil import Perfil
from app.models.conversation import Conversation, Message
from app.schemas.chat_p2p import ConversationOut, MessageCreate, MessageOut, ChatStartRequest
from app.services.websocket_manager import manager

router = APIRouter(tags=["chat_p2p"])

@router.post("/conversations", response_model=ConversationOut)
async def start_or_get_conversation(
    request: ChatStartRequest,
    current_user: Usuario = Depends(get_current_user),
    session: AsyncSession = Depends(get_db)
):
    # Find target user
    result = await session.execute(select(Usuario).where(Usuario.username == request.target_username))
    target_user = result.scalars().first()

    if not target_user:
        raise HTTPException(status_code=404, detail="User not found")
        
    if target_user.id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot start a conversation with yourself")

    # Check if conversation already exists
    conv_result = await session.execute(
        select(Conversation).where(
            or_(
                and_(Conversation.participant1_id == current_user.id, Conversation.participant2_id == target_user.id),
                and_(Conversation.participant1_id == target_user.id, Conversation.participant2_id == current_user.id)
            )
        )
    )
    conversation = conv_result.scalars().first()

    if not conversation:
        # Create new conversation
        conversation = Conversation(
            participant1_id=current_user.id,
            participant2_id=target_user.id
        )
        session.add(conversation)
        await session.commit()
        await session.refresh(conversation)

    return await _enrich_conversation(conversation, current_user.id, session)


@router.get("/conversations", response_model=List[ConversationOut])
async def get_conversations(
    current_user: Usuario = Depends(get_current_user),
    session: AsyncSession = Depends(get_db)
):
    # Get all conversations for the user
    result = await session.execute(
        select(Conversation)
        .where(
            or_(
                Conversation.participant1_id == current_user.id,
                Conversation.participant2_id == current_user.id
            )
        )
        .order_by(Conversation.updated_at.desc())
    )
    conversations = result.scalars().all()
    
    enriched = []
    for conv in conversations:
        enriched.append(await _enrich_conversation(conv, current_user.id, session))
        
    return enriched


@router.get("/conversations/{conversation_id}/messages", response_model=List[MessageOut])
async def get_messages(
    conversation_id: UUID,
    current_user: Usuario = Depends(get_current_user),
    session: AsyncSession = Depends(get_db)
):
    await _verify_conversation_access(conversation_id, current_user.id, session)
    
    result = await session.execute(
        select(Message)
        .where(Message.conversation_id == conversation_id)
        .order_by(Message.created_at.asc())
    )
    return result.scalars().all()


@router.post("/conversations/{conversation_id}/messages", response_model=MessageOut)
async def send_message(
    conversation_id: UUID,
    message: MessageCreate,
    current_user: Usuario = Depends(get_current_user),
    session: AsyncSession = Depends(get_db)
):
    conversation = await _verify_conversation_access(conversation_id, current_user.id, session)
    
    new_message = Message(
        conversation_id=conversation_id,
        sender_id=current_user.id,
        content=message.content,
        is_read=False
    )
    session.add(new_message)
    
    # Update conversation's updated_at timestamp
    conversation.updated_at = func.now()
    
    await session.commit()
    await session.refresh(new_message)
    
    # Notify the other user
    other_user_id = conversation.participant2_id if conversation.participant1_id == current_user.id else conversation.participant1_id
    await manager.send_personal_message(
        {"type": "new_message", "conversation_id": str(conversation_id)},
        str(other_user_id)
    )
    
    return new_message


@router.put("/conversations/{conversation_id}/read")
async def mark_as_read(
    conversation_id: UUID,
    current_user: Usuario = Depends(get_current_user),
    session: AsyncSession = Depends(get_db)
):
    await _verify_conversation_access(conversation_id, current_user.id, session)
    
    # Mark messages sent by the OTHER person as read
    await session.execute(
        update(Message)
        .where(
            and_(
                Message.conversation_id == conversation_id,
                Message.sender_id != current_user.id,
                Message.is_read == False
            )
        )
        .values(is_read=True)
    )
    await session.commit()
    return {"success": True}


@router.get("/unread-count")
async def get_unread_count(
    current_user: Usuario = Depends(get_current_user),
    session: AsyncSession = Depends(get_db)
):
    # Find conversations the user is part of
    conv_subquery = select(Conversation.id).where(
        or_(
            Conversation.participant1_id == current_user.id,
            Conversation.participant2_id == current_user.id
        )
    )
    
    # Count unread messages where the user is NOT the sender
    result = await session.execute(
        select(func.count(Message.id)).where(
            and_(
                Message.conversation_id.in_(conv_subquery),
                Message.sender_id != current_user.id,
                Message.is_read == False
            )
        )
    )
    count = result.scalar() or 0
    return {"unread_count": count}


@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    token: str,
    session: AsyncSession = Depends(get_db)
):
    try:
        payload = jwt.decode(token, settings.JWT_ACCESS_SECRET_KEY, algorithms=[settings.ENCRYPTION_ALGORITHM])
        username: str = payload.get("sub")
        if not username:
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            return
            
        result = await session.execute(select(Usuario).where(or_(Usuario.username == username, Usuario.email == username)))
        user = result.scalar_one_or_none()
        
        if not user or getattr(user, 'is_deleted', False):
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            return
            
        user_id_str = str(user.id)
        
    except JWTError:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    await manager.connect(websocket, user_id_str)
    try:
        while True:
            data = await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket, user_id_str)


# --- Helper functions ---

async def _verify_conversation_access(conversation_id: UUID, user_id: UUID, session: AsyncSession) -> Conversation:
    result = await session.execute(select(Conversation).where(Conversation.id == conversation_id))
    conversation = result.scalars().first()
    
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
        
    if conversation.participant1_id != user_id and conversation.participant2_id != user_id:
        raise HTTPException(status_code=403, detail="Not a participant in this conversation")
        
    return conversation

async def _enrich_conversation(conversation: Conversation, current_user_id: UUID, session: AsyncSession) -> dict:
    # Determine who the other participant is
    other_user_id = conversation.participant2_id if conversation.participant1_id == current_user_id else conversation.participant1_id
    
    user_result = await session.execute(select(Usuario).where(Usuario.id == other_user_id))
    other_user = user_result.scalars().first()
    
    perfil_result = await session.execute(select(Perfil).where(Perfil.usuario_id == other_user_id))
    other_perfil = perfil_result.scalars().first()
    avatar_url = other_perfil.avatar_url if other_perfil and getattr(other_perfil, 'avatar_url', None) else None
    
    # Get last message
    msg_result = await session.execute(
        select(Message)
        .where(Message.conversation_id == conversation.id)
        .order_by(Message.created_at.desc())
        .limit(1)
    )
    last_message = msg_result.scalars().first()
    
    # Get unread count for this conversation (where sender is NOT current user)
    unread_result = await session.execute(
        select(func.count(Message.id))
        .where(
            and_(
                Message.conversation_id == conversation.id,
                Message.sender_id == other_user_id,
                Message.is_read == False
            )
        )
    )
    unread_count = unread_result.scalar() or 0
    
    # Convert conversation to dict and add extra fields manually
    conv_dict = {
        "id": conversation.id,
        "participant1_id": conversation.participant1_id,
        "participant2_id": conversation.participant2_id,
        "created_at": conversation.created_at,
        "updated_at": conversation.updated_at,
        "other_participant": {
            "id": other_user.id,
            "username": other_user.username,
            "first_name": other_user.first_name,
            "last_name": other_user.last_name,
            "role": other_user.role,
            "userImage": getattr(other_user, 'user_image', None),
            "avatar_url": avatar_url
        } if other_user else None,
        "last_message": last_message,
        "unread_count": unread_count
    }
    
    return conv_dict
