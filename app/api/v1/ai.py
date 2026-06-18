from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
import json
import tempfile
import os
from markitdown import MarkItDown
from openai import OpenAI

from app.dependencies import get_admin_user, get_current_user
from app.ai_management.services import ask_oppy_ai
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.ai_management.config import DEFAULT_MODEL

router = APIRouter(prefix="/ai", tags=["ai"])

class TranslationRequest(BaseModel):
    content: Dict[str, Any]
    target_language: str

class TranslationResponse(BaseModel):
    translated_content: Dict[str, Any]

@router.post("/translate", response_model=TranslationResponse)
async def translate_content(
    request: TranslationRequest,
    db: AsyncSession = Depends(get_db),
    _=Depends(get_admin_user)
):
    # Convert dict to string for the prompt
    content_str = json.dumps(request.content, ensure_ascii=False)
    
    prompt = f"""
Translate the following JSON object values into {request.target_language}.
Return strictly a valid JSON object with the exact same keys as the input.
Do not add markdown formatting like ```json or any other text.
Input JSON:
{content_str}
    """
    
    # We call ask_oppy_ai just like the chat endpoint does, but with our specific prompt
    # We use user_id = "admin_translation" or just pass None
    messages = [{"role": "user", "content": prompt}]
    
    try:
        res = await ask_oppy_ai(
            db=db,
            messages=messages,
            caller="admin_translation",
            model_name=DEFAULT_MODEL,
            expect_json=True
        )
        
        # Parse the result back to dict
        result_text = res.strip()
        if result_text.startswith("```json"):
            result_text = result_text.replace("```json", "").replace("```", "").strip()
            
        translated_dict = json.loads(result_text)
        
        return TranslationResponse(translated_content=translated_dict)
    except Exception as e:
        # Fallback in case of JSON parse error or AI failure
        print(f"Translation Error: {e}")
        return TranslationResponse(translated_content=request.content)

@router.post("/cv-extract")
async def extract_cv_data(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user) # Can be any authenticated user
):
    allowed_extensions = ('.pdf', '.docx', '.txt', '.md', '.png', '.jpg', '.jpeg')
    if not file.filename.lower().endswith(allowed_extensions):
        raise HTTPException(status_code=400, detail="Formato no válido. Sube un PDF, DOCX, TXT, MD o Imagen.")
        
    try:
        # Create a temporary file to save the upload
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_path = temp_file.name

        # Initialize OpenAI client pointed to Gemini
        from app.config import settings
        client = OpenAI(
            api_key=settings.gemini_api_key,
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
        )

        # Convert to Markdown using MarkItDown with Gemini as the LLM plugin for OCR
        md = MarkItDown(llm_client=client, llm_model="gemini-2.5-flash")
        result = md.convert(temp_path, llm_prompt="Por favor, extrae todo el texto de esta imagen exactamente como aparece. PRESERVA EL IDIOMA ORIGINAL. NO TRADUZCAS EL TEXTO.")
        markdown_text = result.text_content

        # Clean up temp file
        os.unlink(temp_path)

        # Build prompt for Gemini
        prompt = f"""
Eres un asistente experto de RRHH. Te entregaré el contenido de un Curriculum Vitae (CV).
Tu tarea es extraer la información relevante y devolver ESTRICTAMENTE un objeto JSON usando el siguiente esquema exacto:
{{
  "datos_contacto": {{ "nombre": "Nombre Completo", "ocupacion": "Cargo o Profesión Principal", "telefono": "Teléfono si existe", "email": "Email si existe", "ubicacion": "Ciudad/País si existe", "linkedin": "URL de LinkedIn si existe" }},
  "proyectos": [ {{ "titulo": "Nombre del Proyecto", "descripcion": "Descripción del Proyecto", "tecnologias": ["Tech1", "Tech2"] }} ],
  "experiencias": [ {{ "empresa": "Nombre de la Empresa", "cargo": "Puesto", "periodo_inicio": "YYYY-MM", "periodo_fin": "YYYY-MM o null si es actual", "descripcion": "Descripción del rol y logros" }} ],
  "estudios": [ {{ "institucion": "Universidad o Instituto", "titulo": "Título obtenido", "anio_obtencion": 2020 }} ]
}}

REGLAS CRÍTICAS:
1. La respuesta debe ser ÚNICAMENTE el objeto JSON en crudo, sin etiquetas como ```json ni comentarios extra.
2. EL IDIOMA FINAL DEL JSON DEBE SER ESPAÑOL. El texto proporcionado a continuación puede haber sido traducido al inglés por error por el sistema de reconocimiento (OCR). SIN IMPORTAR en qué idioma esté el texto de abajo, TÚ DEBES TRADUCIR todo el contenido al ESPAÑOL (cargos, descripciones, instituciones, etc.) al generar el JSON.

Aquí está el CV (que puede tener partes en inglés, pero tú debes devolver el JSON en español):
{markdown_text}
"""

        messages = [{"role": "user", "content": prompt}]
        
        # We call ask_oppy_ai
        res = await ask_oppy_ai(
            db=db,
            messages=messages,
            caller="cv_extractor",
            user_id=current_user.id,
            model_name=DEFAULT_MODEL,
            expect_json=True,
            temperature=0.2 # Lower temperature for better extraction
        )
        
        result_text = res.strip()
        if result_text.startswith("```json"):
            result_text = result_text.replace("```json", "").replace("```", "").strip()
        elif result_text.startswith("```"):
            result_text = result_text.replace("```", "").strip()
            
        extracted_data = json.loads(result_text)
        return extracted_data

    except Exception as e:
        print(f"CV Extraction Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
