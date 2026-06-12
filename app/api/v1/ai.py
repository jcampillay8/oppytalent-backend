from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
import json
import tempfile
import os
from markitdown import MarkItDown

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
    if not file.filename.endswith(('.pdf', '.docx', '.txt', '.md')):
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDF, DOCX, TXT, or MD are allowed.")
        
    try:
        # Create a temporary file to save the upload
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_path = temp_file.name

        # Convert to Markdown using MarkItDown
        md = MarkItDown()
        result = md.convert(temp_path)
        markdown_text = result.text_content

        # Clean up temp file
        os.unlink(temp_path)

        # Build prompt for Gemini
        prompt = f"""
You are an expert HR recruiter AI. I will provide you with a CV in Markdown format.
Extract the relevant information and strictly return a JSON object following this exact schema:
{{
  "datos_contacto": {{ "nombre": "Name", "ocupacion": "Current/Main Job Title", "telefono": "Phone if any" }},
  "proyectos": [ {{ "titulo": "Project Name", "descripcion": "Project Description", "tecnologias": ["Tech1", "Tech2"] }} ],
  "experiencias": [ {{ "empresa": "Company Name", "cargo": "Job Title", "periodo_inicio": "YYYY-MM", "periodo_fin": "YYYY-MM or null if present", "descripcion": "Role description" }} ],
  "estudios": [ {{ "institucion": "University/School", "titulo": "Degree", "anio_obtencion": 2020 }} ]
}}
Ensure the response is ONLY the raw JSON object, without ```json wrappers.

Here is the CV:
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
