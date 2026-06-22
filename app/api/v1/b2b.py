from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from sqlalchemy.orm import selectinload
from app.database import get_db, async_session
from app.dependencies import get_current_user, RequirePermission
from app.models.usuario import Usuario
from app.models.portfolio_document import PortfolioDocument
from app.models.b2b_tribunal import TribunalLog, TribunalParticipant
from app.ai_management.embeddings import generate_embedding
from pydantic import BaseModel
from typing import List, Optional
import asyncio
import random

router = APIRouter(prefix="/b2b", tags=["b2b"])

class SearchQuery(BaseModel):
    query: str
    limit: int = 5

class SearchResult(BaseModel):
    usuario_id: UUID
    first_name: Optional[str]
    last_name: Optional[str]
    username: str
    match_score: float
    # We could also return some sample documents
    
@router.post("/search", response_model=List[SearchResult])
async def search_talent(
    body: SearchQuery,
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(RequirePermission("can_use_b2b_search"))
):
    # Billing / Freemium Control for B2B Search (Check Only)
    if current_user.role != "SUPERADMIN" and not current_user.encrypted_gemini_key:
        if current_user.ai_credits < 1:
            raise HTTPException(status_code=402, detail="Créditos insuficientes para usar el Meta-Reclutador. Adquiere un plan B2B.")

    try:
        # Step A & B: Convert query to vector
        query_embedding = generate_embedding(body.query)
        
        # SUCCESS! Deduct credit safely
        if current_user.role != "SUPERADMIN" and not current_user.encrypted_gemini_key:
            current_user.ai_credits -= 1
            await db.commit()
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al generar embedding de búsqueda: {str(e)}")
        
    # Step C & D: Cosine similarity search grouping by user
    # 1. We calculate distance: PortfolioDocument.embedding.cosine_distance(query_embedding)
    # But we want similarity = 1 - distance
    # And we only want to search users who have is_visible_b2b = True
    # We can do a join with Usuario
    
    distance_expr = PortfolioDocument.embedding.cosine_distance(query_embedding)
    
    # We'll get the top documents, but we want the top N *Users*. 
    # An approach is to calculate the minimum distance (best match) per user.
    stmt = (
        select(
            Usuario.id,
            Usuario.first_name,
            Usuario.last_name,
            Usuario.username,
            func.min(distance_expr).label("best_distance")
        )
        .join(PortfolioDocument, PortfolioDocument.usuario_id == Usuario.id)
        .where(Usuario.is_visible_b2b == True)
        .where(Usuario.is_deleted == False)
        .group_by(Usuario.id)
        .order_by(func.min(distance_expr))
        .limit(body.limit)
    )
    
    result = await db.execute(stmt)
    rows = result.all()
    
    results = []
    for row in rows:
        # Cosine distance is usually between 0 and 2. 
        # Similarity roughly: 1 - distance. For percentage, max(0, (1 - distance) * 100)
        # Note: pgvector cosine distance: 0 means exactly the same, 1 means orthogonal, 2 means exactly opposite
        distance = row.best_distance
        similarity_percentage = max(0.0, (1.0 - distance) * 100.0)
        
        results.append(SearchResult(
            usuario_id=row.id,
            first_name=row.first_name,
            last_name=row.last_name,
            username=row.username,
            match_score=round(similarity_percentage, 2)
        ))
        
    return results

class TribunalQuery(BaseModel):
    question: str
    candidate_ids: List[int]

class CandidateResponse(BaseModel):
    usuario_id: UUID
    username: str
    first_name: Optional[str]
    last_name: Optional[str]
    answer: str

class TribunalResult(BaseModel):
    candidates: List[CandidateResponse]
    moderator_summary: str

class TribunalCandidateQuery(BaseModel):
    question: str
    candidate_id: UUID

@router.post("/tribunal/candidate", response_model=CandidateResponse)
async def tribunal_candidate(
    body: TribunalCandidateQuery,
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(RequirePermission("can_execute_tribunal"))
):
    """Generates the response for a single candidate."""

    if current_user.role != "SUPERADMIN" and not current_user.encrypted_gemini_key:
        if current_user.ai_credits < 1:
            raise HTTPException(status_code=402, detail="Créditos insuficientes para el Tribunal.")
            
    from app.ai_management.services import ask_oppy_ai
    from app.ai_management.config import DEFAULT_MODEL
    from app.services.rate_limit import redis_client
    import asyncio

    try:
        question_embedding = generate_embedding(body.question)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al procesar la pregunta: {str(e)}")

    user_res = await db.execute(select(Usuario).where(Usuario.id == body.candidate_id))
    c_user = user_res.scalar_one_or_none()
    if not c_user or not c_user.is_visible_b2b:
        raise HTTPException(status_code=404, detail="Candidato no disponible.")

    distance_expr = PortfolioDocument.embedding.cosine_distance(question_embedding)
    stmt = (
        select(PortfolioDocument)
        .where(PortfolioDocument.usuario_id == body.candidate_id)
        .order_by(distance_expr)
        .limit(3)
    )
    doc_res = await db.execute(stmt)
    docs = doc_res.scalars().all()
    
    if not docs:
        context_str = "El candidato no tiene portafolio registrado."
    else:
        context_str = "\n".join([d.contenido_texto for d in docs])
    
    pitch_rules = c_user.ai_pitch_rules or []
    pitch_str = ""
    if pitch_rules:
        pitch_str = "\nDirectrices de Venta (Aplica si la pregunta se relaciona):\n"
        for r in pitch_rules:
            pitch_str += f"- Si preguntan sobre '{r.get('keyword', '')}': Argumenta '{r.get('pitch', '')}'.\n"

    prompt = f"""
Eres el "Clon Digital" de {c_user.first_name or c_user.username}. Estás participando en un panel técnico (Tribunal B2B) respondiendo a un Headhunter.
Tu objetivo es responder de forma profesional, demostrando técnicamente tu experiencia.
REGLA CRÍTICA: NO ALUCINES. Basa tu respuesta ESTRICTAMENTE en tu contexto. Si no tienes experiencia directa, admite lo que sabes y cómo lo abordarías.
{pitch_str}

TU CONTEXTO PROFESIONAL:
{context_str}

PREGUNTA DEL RECLUTADOR:
{body.question}
"""
    messages = [{"role": "user", "content": prompt}]
    
    try:
        async with redis_client.lock("gemini_global_api_lock", timeout=15):
            await asyncio.sleep(0.5)
            answer = await ask_oppy_ai(
                db=db,
                messages=messages,
                caller="b2b_tribunal_candidate",
                user_id=current_user.id, 
                model_name=DEFAULT_MODEL,
                temperature=0.0
            )
    except Exception as e:
        answer = f"Error al generar respuesta: {str(e)}"

    return CandidateResponse(
        usuario_id=c_user.id,
        username=c_user.username,
        first_name=c_user.first_name,
        last_name=c_user.last_name,
        answer=answer
    )

class ModeratorQuery(BaseModel):
    question: str
    candidates: List[CandidateResponse]

class ModeratorResponse(BaseModel):
    moderator_summary: str

async def generate_talent_feedback(log_id: UUID):
    """Background task to generate personalized feedback for each candidate in a Tribunal."""
    from app.ai_management.services import ask_oppy_ai
    from app.ai_management.config import DEFAULT_MODEL
    
    async with async_session() as session:
        t_log = await session.execute(
            select(TribunalLog).options(selectinload(TribunalLog.participants)).where(TribunalLog.id == log_id)
        )
        t_log = t_log.scalar_one_or_none()
        if not t_log: return
        
        for p in t_log.participants:
            prompt = f"""
Has participado como el Clon Digital B2B de un talento en un Tribunal.
Pregunta del Reclutador: {t_log.question}
Tu Respuesta: {p.clone_answer}
Veredicto del Moderador: {t_log.moderator_summary}

Tu objetivo: Darle feedback constructivo y privado al talento humano sobre por qué respondiste así, qué faltó en su contexto/portafolio para dar una mejor respuesta, y cómo puede mejorar su perfil para la próxima vez. 
Escribe en primera persona ("Soy tu Asistente IA. Hoy me preguntaron..."). Sé breve y conciso (máximo 2 párrafos).
"""
            try:
                # Use a specific bot id or general
                feedback = await ask_oppy_ai(
                    db=session,
                    messages=[{"role": "user", "content": prompt}],
                    caller="b2b_talent_feedback",
                    user_id=None, # System cost
                    model_name=DEFAULT_MODEL,
                    temperature=0.4
                )
                p.talent_feedback = feedback
            except Exception as e:
                p.talent_feedback = "Error al generar feedback de mejora."
                
        await session.commit()

@router.post("/tribunal/moderator", response_model=ModeratorResponse)
async def tribunal_moderator(
    body: ModeratorQuery,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(RequirePermission("can_execute_tribunal"))
):

    if current_user.role != "SUPERADMIN" and not current_user.encrypted_gemini_key:
        if current_user.ai_credits < 1:
            raise HTTPException(status_code=402, detail="Créditos insuficientes para el Moderador.")

    from app.ai_management.services import ask_oppy_ai
    from app.ai_management.config import DEFAULT_MODEL
    from app.services.rate_limit import redis_client
    
    shuffled_responses = list(body.candidates)
    random.shuffle(shuffled_responses)
    
    moderator_context = "\n\n---\n\n".join([
        f"CANDIDATO: {r.first_name or r.username}\nRESPUESTA: {r.answer}" 
        for r in shuffled_responses
    ])
    
    moderator_prompt = f"""
Eres el 'Moderador Neutral' de OppyTalent, un sistema de evaluación técnica imparcial de élite.
El reclutador preguntó: "{body.question}"

Respuestas de los candidatos (entregadas en orden aleatorio):
{moderator_context}

INSTRUCCIONES CRÍTICAS CONTRA SESGOS:
1. No asumas que la respuesta más larga es la mejor. Evalúa concisión y precisión técnica.
2. No te dejes influenciar por el orden en que aparecen los candidatos.
3. Ignora el tono excesivamente persuasivo; céntrate exclusivamente en el mérito técnico, viabilidad de la solución y experiencia demostrada en la respuesta.

Tu trabajo es resumir en formato Markdown, de forma 100% objetiva, los puntos fuertes y débiles técnicos de cada candidato según su respuesta.
Destaca quién parece ser el mejor perfil para la pregunta basándote estrictamente en sus respuestas, sin alucinar.
Mantén un tono analítico, profesional y directo al punto.
"""
    try:
        async with redis_client.lock("gemini_global_api_lock", timeout=15):
            await asyncio.sleep(0.5)
            mod_answer = await ask_oppy_ai(
                db=db,
                messages=[{"role": "user", "content": moderator_prompt}],
                caller="b2b_tribunal_moderator",
                user_id=current_user.id,
                model_name=DEFAULT_MODEL,
                temperature=0.2
            )
    except Exception as e:
        mod_answer = f"El moderador no pudo generar su veredicto. Error: {str(e)}"

    # --- PERSISTENCE ---
    t_log = TribunalLog(
        recruiter_id=current_user.id,
        question=body.question,
        moderator_summary=mod_answer
    )
    db.add(t_log)
    await db.flush() # get ID
    
    for c in body.candidates:
        p = TribunalParticipant(
            tribunal_log_id=t_log.id,
            candidate_id=c.usuario_id,
            clone_answer=c.answer
        )
        db.add(p)
        
    await db.commit()
    
    # --- TRIGGER BACKGROUND FEEDBACK ---
    background_tasks.add_task(generate_talent_feedback, t_log.id)

    return ModeratorResponse(moderator_summary=mod_answer)

class TribunalHistoryResponse(BaseModel):
    id: UUID
    question: str
    moderator_summary: str
    created_at: str

@router.get("/tribunals/history", response_model=List[TribunalHistoryResponse])
async def get_tribunal_history(
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(RequirePermission("can_execute_tribunal"))
):
    """Returns the history of tribunals for a recruiter."""
    stmt = select(TribunalLog).where(TribunalLog.recruiter_id == current_user.id).order_by(TribunalLog.created_at.desc())
    res = await db.execute(stmt)
    logs = res.scalars().all()
    
    return [
        TribunalHistoryResponse(
            id=log.id,
            question=log.question,
            moderator_summary=log.moderator_summary,
            created_at=log.created_at.isoformat()
        )
        for log in logs
    ]

class TalentFeedbackResponse(BaseModel):
    id: UUID
    question: str
    clone_answer: str
    talent_feedback: Optional[str]
    created_at: str

@router.get("/tribunals/talent-feedback", response_model=List[TalentFeedbackResponse])
async def get_talent_feedback(
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(RequirePermission("can_view_own_feedback"))
):
    """Returns the feedback logs for a talent's clone."""
    stmt = select(TribunalParticipant).options(selectinload(TribunalParticipant.tribunal_log)).where(
        TribunalParticipant.candidate_id == current_user.id
    ).order_by(TribunalParticipant.created_at.desc())
    
    res = await db.execute(stmt)
    participants = res.scalars().all()
    
    return [
        TalentFeedbackResponse(
            id=p.id,
            question=p.tribunal_log.question,
            clone_answer=p.clone_answer,
            talent_feedback=p.talent_feedback,
            created_at=p.created_at.isoformat()
        )
        for p in participants
    ]

class DemandInsight(BaseModel):
    skill: str
    trend: str # "Alta Demanda ↑", "Estable →", "Baja Demanda ↓"
    percentage: int
    color_class: str

class DemandResponse(BaseModel):
    total_searches: int
    insights: List[DemandInsight]
    suggestion: str

@router.get("/insights/demand", response_model=DemandResponse)
async def get_demand_insights(
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(RequirePermission("can_view_demand"))
):
    """
    Retorna analítica sobre lo que están buscando los reclutadores.
    Actualmente devuelve datos simulados del mercado global para resolver 
    el "Cold Start Problem", pero está estructurado para escalar a datos 
    reales de B2BSearchLog en el futuro.
    """
    
    # In the future:
    # 1. Query B2BSearchLog for the last 7 days.
    # 2. If count < 100, merge with Global Market Data.
    # 3. If count >= 100, return purely organic platform data.
    
    # Simulated Global Tech Market Data (Cold Start Mitigation)
    return DemandResponse(
        total_searches=420,
        insights=[
            DemandInsight(
                skill="React / Next.js",
                trend="Alta Demanda ↑",
                percentage=85,
                color_class="emerald-500"
            ),
            DemandInsight(
                skill="Python / FastAPI",
                trend="Estable →",
                percentage=65,
                color_class="primary"
            ),
            DemandInsight(
                skill="Ingeniería Cloud (AWS/GCP)",
                trend="Alta Demanda ↑",
                percentage=78,
                color_class="purple-500"
            )
        ],
        suggestion="La tendencia marca un fuerte crecimiento en Cloud y SSR. Te sugerimos subir un proyecto demostrando despliegues Serverless o en contenedores."
    )

@router.post("/qa/reset-credits")
async def qa_reset_credits(
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Ruta exclusiva para el Owner (Testing/QA).
    Permite recargar créditos instantáneamente mientras hace pruebas de impersonación.
    """
    if current_user.role != "SUPERADMIN":
        raise HTTPException(status_code=403, detail="Esta ruta es exclusiva para el equipo de QA/Owner.")
        
    current_user.ai_credits += 10
    await db.commit()
    
    return {"message": f"Se han recargado 10 créditos. Total actual: {current_user.ai_credits}"}
