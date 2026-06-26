from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import or_, and_, update, func
from app.database import get_db
from app.models.usuario import Usuario
from app.models.networking import NetworkConnection, ConnectionStatus
from app.dependencies import get_current_user
import uuid
from datetime import datetime, timedelta
from app.models.networking import NetworkSuggestion
from app.models.perfil import Perfil
from app.models.conversation import Conversation, Message

router = APIRouter(prefix="/network", tags=["Network"])

@router.post("/connect/{user_id}", summary="Send connection request")
async def send_connection_request(
    user_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    if current_user.id == user_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot connect to yourself")

    # Check if a connection already exists
    stmt = select(NetworkConnection).where(
        or_(
            and_(NetworkConnection.requester_id == current_user.id, NetworkConnection.addressee_id == user_id),
            and_(NetworkConnection.requester_id == user_id, NetworkConnection.addressee_id == current_user.id)
        )
    )
    result = await db.execute(stmt)
    existing_connection = result.scalars().first()

    if existing_connection:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Connection already exists with status: {existing_connection.status}")

    new_connection = NetworkConnection(
        requester_id=current_user.id,
        addressee_id=user_id,
        status=ConnectionStatus.PENDING
    )
    db.add(new_connection)
    await db.commit()
    await db.refresh(new_connection)
    return {"message": "Connection request sent", "id": new_connection.id}


@router.put("/accept/{connection_id}", summary="Accept connection request")
async def accept_connection(
    connection_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    stmt = select(NetworkConnection).where(
        NetworkConnection.id == connection_id,
        NetworkConnection.addressee_id == current_user.id,
        NetworkConnection.status == ConnectionStatus.PENDING
    )
    result = await db.execute(stmt)
    connection = result.scalars().first()

    if not connection:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pending connection request not found")

    connection.status = ConnectionStatus.ACCEPTED
    await db.commit()

    # Automatically send a system message from current_user to the requester
    # First, ensure conversation exists
    conv_stmt = select(Conversation).where(
        or_(
            and_(Conversation.participant1_id == current_user.id, Conversation.participant2_id == connection.requester_id),
            and_(Conversation.participant1_id == connection.requester_id, Conversation.participant2_id == current_user.id)
        )
    )
    conv_result = await db.execute(conv_stmt)
    conversation = conv_result.scalars().first()

    if not conversation:
        conversation = Conversation(
            participant1_id=current_user.id,
            participant2_id=connection.requester_id
        )
        db.add(conversation)
        await db.commit()
        await db.refresh(conversation)

    # Create message
    auto_msg = Message(
        conversation_id=conversation.id,
        sender_id=current_user.id,
        content="¡Hola! He aceptado tu solicitud de conexión. Ya somos parte de la misma red profesional en OppyTalent.",
        is_read=False
    )
    db.add(auto_msg)
    
    # Update conversation last_message_at
    conversation.last_message_at = func.now()
    await db.commit()
    await db.refresh(auto_msg)

    # Try to notify the requester via websocket
    try:
        from app.services.websocket_manager import manager
        await manager.send_personal_message(
            {"type": "new_message", "message": "Solicitud de red aceptada"},
            connection.requester_id
        )
    except Exception as e:
        pass

    return {"message": "Connection accepted"}


@router.put("/reject/{connection_id}", summary="Reject connection request")
async def reject_connection(
    connection_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    stmt = select(NetworkConnection).where(
        NetworkConnection.id == connection_id,
        NetworkConnection.addressee_id == current_user.id,
        NetworkConnection.status == ConnectionStatus.PENDING
    )
    result = await db.execute(stmt)
    connection = result.scalars().first()

    if not connection:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pending connection request not found")

    connection.status = ConnectionStatus.REJECTED
    await db.commit()
    return {"message": "Connection rejected"}


@router.get("/connections", summary="List accepted connections")
async def list_connections(
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    stmt = select(NetworkConnection).where(
        or_(
            NetworkConnection.requester_id == current_user.id,
            NetworkConnection.addressee_id == current_user.id
        ),
        NetworkConnection.status == ConnectionStatus.ACCEPTED
    )
    result = await db.execute(stmt)
    connections = result.scalars().all()
    
    # Format the response
    formatted_connections = []
    for conn in connections:
        other_user_id = conn.addressee_id if conn.requester_id == current_user.id else conn.requester_id
        other_user = await db.get(Usuario, other_user_id)
        if other_user:
            stmt = select(Perfil).where(Perfil.usuario_id == other_user_id)
            result_perfil = await db.execute(stmt)
            perfil = result_perfil.scalars().first()
            
            formatted_connections.append({
                "connection_id": conn.id,
                "connected_user_id": other_user_id,
                "affinity_score": conn.affinity_score,
                "connected_since": conn.created_at,
                "user": {
                    "first_name": other_user.first_name,
                    "last_name": other_user.last_name,
                    "username": other_user.username,
                    "user_image": perfil.avatar_url if perfil and perfil.avatar_url else other_user.user_image,
                    "occupation": perfil.ocupacion if perfil else None
                }
            })
    return formatted_connections


@router.get("/pending", summary="List pending connection requests")
async def list_pending_requests(
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    stmt = select(NetworkConnection).where(
        NetworkConnection.addressee_id == current_user.id,
        NetworkConnection.status == ConnectionStatus.PENDING
    )
    result = await db.execute(stmt)
    pending = result.scalars().all()
    
    formatted_pending = []
    for conn in pending:
        # Include requester info
        requester = await db.get(Usuario, conn.requester_id)
        if requester:
            stmt = select(Perfil).where(Perfil.usuario_id == requester.id)
            result_perfil = await db.execute(stmt)
            perfil = result_perfil.scalars().first()
            
            formatted_pending.append({
                "connection_id": conn.id,
                "requester_id": conn.requester_id,
                "affinity_score": conn.affinity_score,
                "created_at": conn.created_at,
                "requester": {
                    "first_name": requester.first_name,
                    "last_name": requester.last_name,
                    "username": requester.username,
                    "user_image": perfil.avatar_url if perfil and perfil.avatar_url else requester.user_image,
                    "occupation": perfil.ocupacion if perfil else None
                }
            })
    return formatted_pending


@router.get("/status/{target_user_id}", summary="Check connection status with a user")
async def check_connection_status(
    target_user_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    if current_user.id == target_user_id:
        return {"status": "SELF"}

    stmt = select(NetworkConnection).where(
        or_(
            and_(NetworkConnection.requester_id == current_user.id, NetworkConnection.addressee_id == target_user_id),
            and_(NetworkConnection.requester_id == target_user_id, NetworkConnection.addressee_id == current_user.id)
        )
    )
    result = await db.execute(stmt)
    conn = result.scalars().first()

    if not conn:
        return {"status": "NONE"}

    if conn.status == ConnectionStatus.ACCEPTED:
        return {"status": "ACCEPTED"}
    elif conn.status == ConnectionStatus.PENDING:
        if conn.requester_id == current_user.id:
            return {"status": "PENDING"}
        else:
            return {"status": "PENDING_RECEIVED"}
    elif conn.status == ConnectionStatus.REJECTED:
        return {"status": "REJECTED"}
    
    return {"status": "NONE"}


from sqlalchemy import text
from app.config import settings

@router.get("/degrees/{target_user_id}", summary="Get connection degree between current user and target user")
async def get_connection_degree(
    target_user_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    if current_user.id == target_user_id:
        return {"degree": 0}

    schema_prefix = f"{settings.DB_SCHEMA}." if settings.DB_SCHEMA else ""
    
    # CTE recursivo para calcular los grados de separación hasta un máximo de 3
    query = text(f"""
        WITH RECURSIVE degrees AS (
            -- Caso base: Nivel 1 (Conexiones directas)
            SELECT 
                CASE 
                    WHEN requester_id = :start_id THEN addressee_id 
                    ELSE requester_id 
                END as connected_id,
                1 as degree,
                ARRAY[CASE WHEN requester_id = :start_id THEN addressee_id ELSE requester_id END] as path
            FROM {schema_prefix}network_connections
            WHERE (requester_id = :start_id OR addressee_id = :start_id)
              AND status = 'ACCEPTED'

            UNION

            -- Caso recursivo: Nivel 2 y 3
            SELECT 
                CASE 
                    WHEN nc.requester_id = d.connected_id THEN nc.addressee_id 
                    ELSE nc.requester_id 
                END as connected_id,
                d.degree + 1,
                d.path || (CASE WHEN nc.requester_id = d.connected_id THEN nc.addressee_id ELSE nc.requester_id END)
            FROM {schema_prefix}network_connections nc
            INNER JOIN degrees d ON (nc.requester_id = d.connected_id OR nc.addressee_id = d.connected_id)
            WHERE nc.status = 'ACCEPTED'
              AND d.degree < 3
              AND NOT (CASE WHEN nc.requester_id = d.connected_id THEN nc.addressee_id ELSE nc.requester_id END) = ANY(d.path)
              AND NOT (CASE WHEN nc.requester_id = d.connected_id THEN nc.addressee_id ELSE nc.requester_id END) = :start_id
        )
        SELECT MIN(degree) as min_degree
        FROM degrees
        WHERE connected_id = :target_id;
    """)

    result = await db.execute(query, {"start_id": current_user.id, "target_id": target_user_id})
    row = result.fetchone()

    if row and row.min_degree is not None:
        return {"degree": row.min_degree}
    else:
        return {"degree": None, "message": "No connection found within 3 degrees"}

@router.get("/feed", summary="Get personalized network feed")
async def get_network_feed(
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
    limit: int = 50,
    offset: int = 0
):
    schema_prefix = f"{settings.DB_SCHEMA}." if settings.DB_SCHEMA else ""
    
    query = text(f"""
        WITH RECURSIVE degrees AS (
            -- Self
            SELECT CAST(:start_id AS UUID) as connected_id, 0 as degree, ARRAY[CAST(:start_id AS UUID)] as path
            
            UNION
            
            -- Level 1
            SELECT 
                CASE WHEN requester_id = :start_id THEN addressee_id ELSE requester_id END,
                1,
                ARRAY[CASE WHEN requester_id = :start_id THEN addressee_id ELSE requester_id END]
            FROM {schema_prefix}network_connections
            WHERE (requester_id = :start_id OR addressee_id = :start_id) AND status = 'ACCEPTED'

            UNION

            -- Level 2
            SELECT 
                CASE WHEN nc.requester_id = d.connected_id THEN nc.addressee_id ELSE nc.requester_id END,
                d.degree + 1,
                d.path || (CASE WHEN nc.requester_id = d.connected_id THEN nc.addressee_id ELSE nc.requester_id END)
            FROM {schema_prefix}network_connections nc
            INNER JOIN degrees d ON (nc.requester_id = d.connected_id OR nc.addressee_id = d.connected_id)
            WHERE nc.status = 'ACCEPTED' AND d.degree < 2
              AND NOT (CASE WHEN nc.requester_id = d.connected_id THEN nc.addressee_id ELSE nc.requester_id END) = ANY(d.path)
              AND NOT (CASE WHEN nc.requester_id = d.connected_id THEN nc.addressee_id ELSE nc.requester_id END) = :start_id
        ),
        min_degrees AS (
            SELECT connected_id, MIN(degree) as degree FROM degrees GROUP BY connected_id
        )
        SELECT 
            fe.id, fe.user_id, fe.event_type, fe.entity_id, fe.created_at,
            u.first_name, u.last_name, u.username, u.user_image,
            md.degree
        FROM {schema_prefix}feed_events fe
        JOIN min_degrees md ON fe.user_id = md.connected_id
        JOIN {schema_prefix}usuarios u ON fe.user_id = u.id
        ORDER BY fe.created_at DESC
        LIMIT :limit OFFSET :offset;
    """)

    result = await db.execute(query, {"start_id": current_user.id, "limit": limit, "offset": offset})
    rows = result.fetchall()

    feed = []
    for row in rows:
        feed.append({
            "id": row.id,
            "user_id": row.user_id,
            "event_type": row.event_type,
            "entity_id": row.entity_id,
            "created_at": row.created_at,
            "user": {
                "first_name": row.first_name,
                "last_name": row.last_name,
                "username": row.username,
                "user_image": row.user_image,
                "degree": row.degree
            }
        })

    return feed


@router.get("/suggestions", summary="Get AI network suggestions")
async def get_network_suggestions(
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    seven_days_ago = datetime.now() - timedelta(days=7)
    
    stmt = select(NetworkSuggestion).where(
        NetworkSuggestion.user_id == current_user.id,
        NetworkSuggestion.created_at >= seven_days_ago
    )
    result = await db.execute(stmt)
    existing_suggestions = result.scalars().all()
    
    if existing_suggestions:
        output = []
        for s in existing_suggestions:
            s_user = await db.get(Usuario, s.suggested_user_id)
            if s_user:
                output.append({
                    "suggested_user_id": s.suggested_user_id,
                    "reason": s.reason,
                    "affinity_score": s.affinity_score,
                    "user": {
                        "first_name": s_user.first_name,
                        "last_name": s_user.last_name,
                        "username": s_user.username,
                        "user_image": s_user.user_image,
                        "occupation": s_user.occupation
                    }
                })
        return output
        
    schema_prefix = f"{settings.DB_SCHEMA}." if settings.DB_SCHEMA else ""
    
    query = text(f"""
        WITH RECURSIVE degrees AS (
            SELECT CAST(:start_id AS UUID) as connected_id, 0 as degree, ARRAY[CAST(:start_id AS UUID)] as path
            UNION
            SELECT CASE WHEN requester_id = :start_id THEN addressee_id ELSE requester_id END, 1, ARRAY[CASE WHEN requester_id = :start_id THEN addressee_id ELSE requester_id END]
            FROM {schema_prefix}network_connections WHERE (requester_id = :start_id OR addressee_id = :start_id) AND status = 'ACCEPTED'
            UNION
            SELECT CASE WHEN nc.requester_id = d.connected_id THEN nc.addressee_id ELSE nc.requester_id END, d.degree + 1, d.path || (CASE WHEN nc.requester_id = d.connected_id THEN nc.addressee_id ELSE nc.requester_id END)
            FROM {schema_prefix}network_connections nc
            INNER JOIN degrees d ON (nc.requester_id = d.connected_id OR nc.addressee_id = d.connected_id)
            WHERE nc.status = 'ACCEPTED' AND d.degree < 3 AND NOT (CASE WHEN nc.requester_id = d.connected_id THEN nc.addressee_id ELSE nc.requester_id END) = ANY(d.path) AND NOT (CASE WHEN nc.requester_id = d.connected_id THEN nc.addressee_id ELSE nc.requester_id END) = :start_id
        ),
        min_degrees AS (
            SELECT connected_id, MIN(degree) as degree FROM degrees GROUP BY connected_id
        )
        SELECT md.connected_id, md.degree, u.username, u.occupation, u.about
        FROM min_degrees md
        JOIN {schema_prefix}usuarios u ON md.connected_id = u.id
        WHERE md.degree IN (2, 3)
        LIMIT 20;
    """)
    res = await db.execute(query, {"start_id": current_user.id})
    candidates = res.fetchall()
    
    if not candidates:
         return []
         
    candidates_info = []
    for c in candidates:
        candidates_info.append(f"ID: {c.connected_id} | Rol: {c.occupation} | Acerca de: {c.about} | Grado de separación: {c.degree}")
        
    prompt_context = f"""
    Eres un Headhunter de Élite e IA Matchmaker para una red social profesional.
    El usuario actual es:
    Rol: {current_user.occupation}
    Acerca de: {current_user.about}
    
    Aquí tienes una lista de perfiles que están a 2 o 3 grados de separación en su red de contactos:
    {chr(10).join(candidates_info)}
    
    Tu tarea: Selecciona hasta 3 usuarios de esta lista con los que el usuario actual tendría el mayor beneficio profesional si conectan (sinergia técnica, complementariedad o roles compatibles). 
    Debes explicar por qué recomiendas cada conexión en un tono entusiasta y profesional.
    
    Retorna estrictamente un JSON list con este esquema:
    [
      {{
        "suggested_user_id": "UUID",
        "reason": "Explicación breve de 2 líneas de por qué hacer match.",
        "affinity_score": 0.85
      }}
    ]
    """
    
    messages = [
        {"role": "system", "content": "Eres el motor de recomendaciones B2B de OppyTalent. Devuelve un JSON válido siempre."},
        {"role": "user", "content": prompt_context}
    ]
    
    from app.ai_management.services import ask_oppy_ai
    import json
    
    ai_res_str = await ask_oppy_ai(
        db=db,
        messages=messages,
        caller="network_suggestions",
        user_id=current_user.id,
        expect_json=True
    )
    
    try:
        suggestions_data = json.loads(ai_res_str)
    except json.JSONDecodeError:
        return []
        
    output = []
    for sd in suggestions_data:
        try:
            s_uid = uuid.UUID(sd.get("suggested_user_id"))
            ns = NetworkSuggestion(
                user_id=current_user.id,
                suggested_user_id=s_uid,
                reason=sd.get("reason", "Afinidad profesional"),
                affinity_score=sd.get("affinity_score", 0.5)
            )
            db.add(ns)
            
            s_user = await db.get(Usuario, s_uid)
            if s_user:
                output.append({
                    "suggested_user_id": s_uid,
                    "reason": ns.reason,
                    "affinity_score": ns.affinity_score,
                    "user": {
                        "first_name": s_user.first_name,
                        "last_name": s_user.last_name,
                        "username": s_user.username,
                        "user_image": s_user.user_image,
                        "occupation": s_user.occupation
                    }
                })
        except Exception as e:
            continue
            
    await db.commit()
    return output

