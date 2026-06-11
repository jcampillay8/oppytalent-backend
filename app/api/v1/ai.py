from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import Dict, Any
import json

from app.dependencies import get_admin_user
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
