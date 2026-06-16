from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc, or_
from typing import List
import httpx
from bs4 import BeautifulSoup

from app.database import get_db
from app.models.usuario import Usuario
from app.models.cover_letter import CoverLetter
from app.schemas.cover_letter import CoverLetterResponse, CoverLetterGenerateRequest, SendEmailRequest
from app.dependencies import get_current_user
from app.ai_management.services import ask_oppy_ai

router = APIRouter()

@router.post("/cover-letters/generate/{username}", response_model=CoverLetterResponse)
async def generate_cover_letter(
    username: str,
    request_data: CoverLetterGenerateRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Generates a cover letter for the given user based on a job description.
    This uses the user's AI credits/API Key.
    """
    # 1. Fetch user to check existence and get data context
    result = await db.execute(
        select(Usuario).where(
            or_(
                Usuario.username == username,
                Usuario.email == username,
                Usuario.username.ilike(f"{username}@%")
            )
        )
    )
    portfolio_user = result.scalar_one_or_none()
    
    if not portfolio_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # 2. Extract job description if it's a URL
    job_description_text = request_data.job_description
    if job_description_text.startswith("http://") or job_description_text.startswith("https://"):
        try:
            async with httpx.AsyncClient(follow_redirects=True, timeout=10.0) as client:
                headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
                resp = await client.get(job_description_text, headers=headers)
                resp.raise_for_status()
                soup = BeautifulSoup(resp.text, "html.parser")
                # Remove scripts and styles
                for script in soup(["script", "style"]):
                    script.extract()
                extracted_text = soup.get_text(separator=" ", strip=True)
                job_description_text = extracted_text[:15000] # Limit to 15k chars
        except Exception as e:
            # If scraping fails, tell the user to paste the text instead
            raise HTTPException(status_code=400, detail="No pudimos leer la URL (es probable que tenga bloqueos anti-bot). Por favor, copia y pega el texto de la oferta en lugar del enlace.")

    # 3. Build the AI context & prompt
    
    system_prompt = (
        f"Eres el representante profesional y gemelo digital de {portfolio_user.first_name or portfolio_user.username}. "
        "Tu tarea es generar una 'Cover Letter' (Carta de presentación) profesional, persuasiva y formal "
        "dirigida a los reclutadores de una oferta de empleo.\n"
        "Debes analizar la oferta de empleo proporcionada, analizar el portafolio del usuario, "
        "y redactar una carta en primera persona (como si fueras el talento) demostrando por qué "
        "tu experiencia es el ajuste perfecto (fit) para la vacante.\n"
        "Si el cargo provisto es 'Oferta desde URL', debes deducir el cargo real y la empresa desde la descripción de la oferta.\n"
        "Al principio de tu respuesta debes indicar explícitamente el 'Nivel de Match' estimado (ej: 85% Match) basándote "
        "en las habilidades del usuario vs los requisitos del cargo. Luego, deja un salto de línea y comienza la carta. "
        "La carta debe estar en formato Markdown legible."
    )
    
    user_prompt = (
        f"Genera una Cover Letter para la siguiente oferta de trabajo:\n"
        f"Cargo: {request_data.job_title}\n"
        f"Empresa: {request_data.company_name or 'No especificada'}\n"
        f"Descripción de la oferta:\n{job_description_text}\n"
    )
    
    # 3. Call AI Service (Uses billing fork internally!)
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
    try:
        generated_letter_text = await ask_oppy_ai(
            messages=messages,
            caller="cover_letter_generator",
            db=db,
            temperature=0.7
        )
    except Exception as e:
        # Pasa los errores de la IA directo (como 402 Payment Required)
        raise e
    
    # 4. Save to Database
    new_letter = CoverLetter(
        usuario_id=portfolio_user.id,
        job_title=request_data.job_title,
        company_name=request_data.company_name,
        job_description=request_data.job_description,
        generated_letter=generated_letter_text,
        generated_by=request_data.generated_by,
        recruiter_email=request_data.recruiter_email
    )
    db.add(new_letter)
    await db.commit()
    await db.refresh(new_letter)
    
    return new_letter

@router.get("/cover-letters", response_model=List[CoverLetterResponse])
async def get_my_cover_letters(
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """Obtiene las cartas de presentación guardadas del usuario autenticado."""
    result = await db.execute(
        select(CoverLetter)
        .where(CoverLetter.usuario_id == current_user.id)
        .order_by(desc(CoverLetter.created_at))
    )
    return result.scalars().all()

@router.delete("/cover-letters/{letter_id}")
async def delete_cover_letter(
    letter_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    result = await db.execute(
        select(CoverLetter).where(CoverLetter.id == letter_id, CoverLetter.usuario_id == current_user.id)
    )
    letter = result.scalar_one_or_none()
    
    if not letter:
        raise HTTPException(status_code=404, detail="Carta no encontrada")
        
    await db.delete(letter)
    await db.commit()
    return {"message": "Cover letter deleted"}

import os

@router.post("/cover-letters/{letter_id}/send-email")
async def send_cover_letter_email(
    letter_id: int,
    request: SendEmailRequest,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(CoverLetter).where(CoverLetter.id == letter_id))
    letter = result.scalar_one_or_none()
    
    if not letter:
        raise HTTPException(status_code=404, detail="Carta no encontrada")
        
    resend_key = os.getenv("RESEND_API_KEY")
    if not resend_key:
        raise HTTPException(status_code=500, detail="RESEND_API_KEY no configurado en el servidor")
        
    html_content = f"""
    <h2>Tu Carta de Presentación ha sido generada</h2>
    <p>Hola,</p>
    <p>Aquí tienes la carta de presentación generada para la posición de <strong>{letter.job_title}</strong>.</p>
    <hr>
    <div style="white-space: pre-wrap; font-family: 'Times New Roman', serif;">
    {letter.generated_letter}
    </div>
    """
    
    payload = {
        "from": os.getenv("EMAIL_FROM", "OppyChat Support <support@oppychat.com>"),
        "to": [request.email],
        "subject": f"Cover Letter: {letter.job_title}",
        "html": html_content
    }
    
    # If base64 PDF is provided, attach it
    if hasattr(request, 'pdf_base64') and request.pdf_base64:
        payload["attachments"] = [
            {
                "filename": f"Cover_Letter_{letter.job_title.replace(' ', '_')}.pdf",
                "content": request.pdf_base64
            }
        ]

    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                "https://api.resend.com/emails",
                headers={"Authorization": f"Bearer {resend_key}"},
                json=payload
            )
            resp.raise_for_status()
    except Exception as e:
        print(f"Error enviando correo con Resend: {e}")
        raise HTTPException(status_code=500, detail="No se pudo enviar el correo.")
        
    return {"message": "Email sent successfully"}
