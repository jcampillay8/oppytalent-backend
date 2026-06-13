from fastapi import APIRouter, HTTPException, status, Depends, Request
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List
from datetime import datetime

from app.ai_management.services import ask_oppy_ai
from app.ai_management.config import DEFAULT_MODEL
from app.services.json_sync import load_json_context
from app.database import get_db
from app.models.chat_log import ChatLog
from app.dependencies import get_admin_user, get_current_user
from app.models.usuario import Usuario
from app.services.rate_limit import check_rate_limit

router = APIRouter(prefix="/chat", tags=["chat"])





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

4. REGLA DE ORO DE NAVEGACIÓN OBLIGATORIA (BOTONES INTERACTIVOS SI/NO):
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

    context = load_json_context(portfolio_user.id)
    
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
