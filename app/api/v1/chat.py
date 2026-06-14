from fastapi import APIRouter, HTTPException, status, Depends, Request
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List
from datetime import datetime, date
import json

from app.ai_management.services import ask_oppy_ai
from app.ai_management.config import DEFAULT_MODEL
from app.database import get_db
from app.models.chat_log import ChatLog
from app.dependencies import get_admin_user, get_current_user
from app.models.usuario import Usuario
from app.models.perfil import Perfil
from app.models.proyecto import Proyecto
from app.models.experiencia import Experiencia
from app.models.estudio import Estudio
from app.services.rate_limit import check_rate_limit
from app.services.cache import redis_client

router = APIRouter(prefix="/chat", tags=["chat"])

def _serialize(obj):
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    return obj

def _model_to_dict(entity):
    data = {}
    for column in entity.__table__.columns:
        val = getattr(entity, column.name)
        data[column.name] = _serialize(val)
    return data

async def load_db_context(db: AsyncSession, usuario_id: int) -> str:
    cache_key = f"ai_context:{usuario_id}"
    try:
        cached = await redis_client.get(cache_key)
        if cached:
            return cached.decode("utf-8") if isinstance(cached, bytes) else cached
    except Exception:
        pass

    sections = []
    models_mapping = {
        "PERFIL": Perfil,
        "EXPERIENCIAS": Experiencia,
        "PROYECTOS": Proyecto,
        "ESTUDIOS": Estudio
    }
    
    for section_name, model in models_mapping.items():
        query = select(model).where(model.is_active == True, model.usuario_id == usuario_id)
        result = await db.execute(query)
        rows = result.scalars().all()
        if rows:
            data = [_model_to_dict(r) for r in rows]
            sections.append(f"=== {section_name} ===\n{json.dumps(data, indent=2, ensure_ascii=False)}")
            
    context_str = "\n\n".join(sections)
    
    try:
        await redis_client.setex(cache_key, 1800, context_str)
    except Exception:
        pass
        
    return context_str

class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    username: str
    messages: list[ChatMessage]


class ChatResponse(BaseModel):
    content: str
    log_id: int


class ChatLogResponse(BaseModel):
    id: int
    ip_address: str | None
    city: str | None = None
    region: str | None = None
    country: str | None = None
    user_message: str
    ai_response: str
    clicked_link: str | None = None
    created_at: datetime


SYSTEM_PROMPT_TEMPLATE = """Eres el asistente virtual del portafolio profesional de {full_name}. Tu objetivo es responder preguntas de reclutadores, Tech Leads y gerentes basándote estrictamente en los JSON de su portafolio. Tu meta no es solo informar, sino defender y vender su perfil de forma profesional, técnica y ejecutiva, destacando sus KPIs de rendimiento y decisiones de arquitectura.

Directrices obligatorias de comportamiento:

1. NADA DE "TONO ASISTENTE":
   No uses frases como "Basándome en los datos...", "Según la información que tengo aquí...", "Mira, analizando...". Habla con propiedad ejecutiva y directa como si fueras su representante profesional.

2. PROHIBIDOS LOS ADJETIVOS VAGOS:
   Elimina adjetivos vagos. La capacidad técnica se demuestra con hechos concretos del stack y herramientas mencionadas en el perfil.

3. OBLIGACIÓN DE CITAR KPIs:
   Cada vez que mencionas una fortaleza, proyecto o experiencia, DEBES extraer y citar métricas duras de los JSON si existen. No basta con describir el proyecto; hay que respaldarlo con números.

4. RESUMEN DE PERFIL DETALLADO (¿Quién es?):
   Si el usuario te pregunta "¿Quién es {full_name}?", "Háblame de {full_name}", o pide un resumen de su perfil, DEBES crear una respuesta rica y descriptiva utilizando los datos de la sección PERFIL y sus experiencias/estudios. No te limites a presentarte a ti mismo. Describe claramente su profesión, años de experiencia (si aplica), su enfoque y sus áreas de especialización.

5. REGLA DE ORO DE NAVEGACIÓN OBLIGATORIA (BOTONES INTERACTIVOS SI/NO):
   Siempre que el usuario pregunte por un proyecto o experiencia laboral en particular, o tu respuesta se centre, describa o mencione de forma relevante uno de ellos, DEBES de forma MÁXIMA y OBLIGATORIA finalizar el mensaje (en una línea nueva al final) con la pregunta interactiva exacta.
   Usa estrictamente las IDs reales mapeadas de la base de datos JSON:
   
   - Si tu respuesta describe, explica o menciona un proyecto, finaliza exactamente con:
     ¿Desea ver el proyecto [Nombre del Proyecto]? [SÍ](/proyecto/[ID_DEL_PROYECTO]) / [NO](#)
     
   - Si tu respuesta describe o menciona una experiencia, finaliza exactamente con:
     ¿Desea ver la experiencia en [Nombre Empresa]? [SÍ](/experiencia/[ID_DE_EXPERIENCIA]) / [NO](#)
   
   - Si el usuario te pregunta por los datos de contacto de {full_name} (email, teléfono, linkedin, github, ciudad, o cómo contactarlo), DEBES finalizar exactamente con:
     ¿Desea ir a la vista de contacto? [SÍ](/contactame) / [NO](#)
   
   Esta directiva es absoluta y prioritaria. Si hablas de cualquiera de estos elementos en tu respuesta, no debes despedirte ni cerrar el mensaje de otra forma; la última línea de tu mensaje debe ser esta pregunta de invitación estructurada con sus respectivos enlaces Markdown.

A continuación tienes los datos completos del portafolio en formato JSON:

{context}

Responde SOLO con información que esté en estos datos. Si te preguntan por alguien que no sea {full_name}, indica amablemente que eres el asistente exclusivo de {full_name}. Sé directo, técnico, ingenioso y profesional."""


@router.post("/", response_model=ChatResponse)
async def chat(payload: ChatRequest, request: Request, db: AsyncSession = Depends(get_db)):
    if not payload.messages:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No messages provided")

    # Extract IP address early for rate limiting
    # 1. Try custom header from frontend Nginx
    ip_address = request.headers.get("X-Original-IP")
    if not ip_address:
        # 2. Try standard Railway/Cloudflare header
        ip_address = request.headers.get("X-Forwarded-For")
        if not ip_address:
            ip_address = request.client.host if request.client else "unknown"
    
    # In case of multiple IPs, take the first one (original client)
    ip_address = ip_address.split(",")[0].strip()

    # Check rate limit (e.g. max 5 requests per 60 seconds)
    await check_rate_limit(ip_address, max_requests=5, window_seconds=60)

    # Fetch the portfolio user first
    from sqlalchemy import or_
    result = await db.execute(
        select(Usuario).where(
            or_(
                Usuario.username == payload.username,
                Usuario.email == payload.username,
                Usuario.username.ilike(f"{payload.username}@%")
            )
        )
    )
    portfolio_user = result.scalar_one_or_none()
    if not portfolio_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Portfolio user not found")

    # Check Authentication
    is_authenticated = False
    authorization = request.headers.get("Authorization")
    if authorization:
        from fastapi.security.utils import get_authorization_scheme_param
        scheme, token = get_authorization_scheme_param(authorization)
        if scheme.lower() == "bearer":
            from jose import jwt
            from app.config import settings
            try:
                jwt_payload = jwt.decode(token, settings.JWT_ACCESS_SECRET_KEY, algorithms=[settings.ENCRYPTION_ALGORITHM])
                if jwt_payload.get("sub"):
                    is_authenticated = True
            except Exception:
                pass
                
    # Enforce Daily Quota for Unauthenticated Users (e.g., 10 messages per IP per Portfolio)
    if not is_authenticated and ip_address and ip_address != "unknown":
        quota_key = f"chat_quota:{ip_address}:{portfolio_user.id}"
        try:
            current_count = await redis_client.incr(quota_key)
            if current_count == 1:
                # Set expiration for 24 hours (86400 seconds)
                await redis_client.expire(quota_key, 86400)
            
            MAX_UNAUTH_MESSAGES = 10
            if current_count > MAX_UNAUTH_MESSAGES:
                fallback_msg = "🤖 Espero haber resuelto tus principales dudas sobre mi perfil profesional. Como mi tiempo de procesamiento en vivo es limitado, te invito a agendar una entrevista directa conmigo o enviarme un mensaje a través de mi [Sección de Contacto](/contactame). ¡Estaré encantado de hablar contigo en persona!"
                return ChatResponse(content=fallback_msg, log_id=0)
        except Exception:
            pass # Ignore redis errors and allow chat if redis fails

    context = await load_db_context(db, portfolio_user.id)
    
    # Get the user's full name to inject in the prompt
    full_name = f"{portfolio_user.first_name} {portfolio_user.last_name}".strip()
    if not full_name:
        full_name = portfolio_user.username.split("@")[0]
        
    system_prompt = SYSTEM_PROMPT_TEMPLATE.format(context=context, full_name=full_name)

    messages_for_ai = [{"role": "system", "content": system_prompt}]
    for m in payload.messages:
        role = "user" if m.role == "user" else "assistant"
        messages_for_ai.append({"role": role, "content": m.content})

    ai_res_content = await ask_oppy_ai(
        db=db,
        messages=messages_for_ai,
        caller="portafolio_chat",
        model_name=DEFAULT_MODEL,
        temperature=0.7,
        expect_json=False
    )

    # Extract last user message
    last_user_msg = "No message"
    for msg in reversed(payload.messages):
        if msg.role == "user":
            last_user_msg = msg.content
            break

    # Fetch location info from ipinfo.io
    city, region, country = None, None, None
    if ip_address and ip_address != "unknown" and ip_address != "127.0.0.1":
        try:
            import httpx
            async with httpx.AsyncClient(timeout=3.0) as client:
                res = await client.get(f"https://ipinfo.io/{ip_address}/json")
                if res.status_code == 200:
                    data = res.json()
                    city = data.get("city")
                    region = data.get("region")
                    country = data.get("country")
        except Exception:
            pass # Ignore errors fetching IP info so chat still works

    # The portfolio_user is already fetched above, we just use its ID

    # Save to database
    chat_log = ChatLog(
        usuario_id=portfolio_user.id,
        ip_address=ip_address,
        city=city,
        region=region,
        country=country,
        user_message=last_user_msg,
        ai_response=ai_res_content
    )
    db.add(chat_log)
    await db.commit()
    await db.refresh(chat_log)

    return ChatResponse(content=ai_res_content, log_id=chat_log.id)

class ChatClickRequest(BaseModel):
    clicked_link: str

@router.patch("/{log_id}/click")
async def register_click(log_id: int, payload: ChatClickRequest, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ChatLog).where(ChatLog.id == log_id))
    chat_log = result.scalar_one_or_none()
    if not chat_log:
        raise HTTPException(status_code=404, detail="Chat log not found")
    
    chat_log.clicked_link = payload.clicked_link
    await db.commit()
    return {"status": "success"}


@router.get("/logs", response_model=List[ChatLogResponse])
async def get_chat_logs(
    limit: int = 100, 
    db: AsyncSession = Depends(get_db), 
    current_user: Usuario = Depends(get_current_user)
):
    result = await db.execute(
        select(ChatLog)
        .where(ChatLog.usuario_id == current_user.id)
        .order_by(ChatLog.created_at.desc())
        .limit(limit)
    )
    logs = result.scalars().all()
    return logs


@router.get("/stats")
async def get_chat_stats(
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    # Get the count of interactions per day for the last 30 days
    query = (
        select(
            func.date(ChatLog.created_at).label('date'),
            func.count(ChatLog.id).label('count')
        )
        .where(ChatLog.usuario_id == current_user.id)
        .group_by(func.date(ChatLog.created_at))
        .order_by(func.date(ChatLog.created_at).asc())
        .limit(30)
    )
    result = await db.execute(query)
    stats = [{"date": str(row.date), "count": row.count} for row in result.all()]
    return stats
