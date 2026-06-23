# app/ai_management/client.py
import time
from typing import Any
from google import genai
from google.genai import types
from .schemas import AIResponse
from app.config import settings

async def call_gemini_api(
    system_instruction: str,
    user_prompt: str,
    model_cfg: Any,
    temperature: float = 0.7,
    expect_json: bool = False,
    user_api_key: str | None = None
) -> AIResponse:
    """Llamada directa a la API de Gemini con cálculo de costos dinámico."""
    
    start_time = time.monotonic()
    api_key_to_use = user_api_key if user_api_key else settings.gemini_api_key
    client = genai.Client(api_key=api_key_to_use)
    
    config = types.GenerateContentConfig(
        system_instruction=system_instruction,
        temperature=temperature,
    )
    if expect_json:
        config.response_mime_type = "application/json"
    
    try:
        response = await client.aio.models.generate_content(
            model=model_cfg.model_name,
            contents=user_prompt,
            config=config
        )
        
        content = response.text
        
        usage = response.usage_metadata
        input_tokens = usage.prompt_token_count if usage else 0
        output_tokens = usage.candidates_token_count if usage else 0
        
    except Exception as e:
        # Re-raise the exception so the orchestrator can catch it and perform retries
        raise e
    
    # CÁLCULO DE COSTO usando los precios de la DB (model_cfg)
    cost = (input_tokens * (model_cfg.input_price_per_million / 1_000_000)) + \
           (output_tokens * (model_cfg.output_price_per_million / 1_000_000))
           
    return AIResponse(
        content=content,
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        total_tokens=input_tokens + output_tokens,
        estimated_cost=cost,
        duration_ms=int((time.monotonic() - start_time) * 1000)
    )
