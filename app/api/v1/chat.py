from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from app.ai_management.client import call_gemini_api
from app.ai_management.config import DEFAULT_MODEL, GEMINI_PRICING
from app.services.json_sync import load_json_context

router = APIRouter(prefix="/chat", tags=["chat"])


class SimpleModelCfg:
    def __init__(self, model_name: str):
        self.model_name = model_name
        self.input_price_per_million = GEMINI_PRICING.get(model_name, {}).get("input_price_per_million", 0)
        self.output_price_per_million = GEMINI_PRICING.get(model_name, {}).get("output_price_per_million", 0)


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: list[ChatMessage]


class ChatResponse(BaseModel):
    content: str


SYSTEM_PROMPT_TEMPLATE = """Eres el asistente virtual del portafolio profesional de Jaime Gabriel Campillay Rojas. Tu objetivo es responder preguntas de reclutadores, Tech Leads y gerentes basándote estrictamente en los JSON de su portafolio. Tu meta no es solo informar, sino defender y vender su perfil de forma profesional, técnica y ejecutiva, destacando sus KPIs de rendimiento y decisiones de arquitectura.

Directrices obligatorias de comportamiento:

1. NADA DE "TONO ASISTENTE":
   No uses frases como "Basándome en los datos...", "Según la información que tengo aquí...", "Mira, analizando...". Habla con propiedad ejecutiva y directa como si fueras su representante profesional.

2. PROHIBIDOS LOS ADJETIVOS VAGOS:
   Elimina "experiencias bastante interesantes", "perfil bien completo", "profesional multifacético", "trayectoria bien completa". La capacidad técnica se demuestra con hechos concretos del stack: FastAPI, React 19, Polars, PostgreSQL, Redis, Docker, Gemini API, etc.

3. OBLIGACIÓN DE CITAR KPIs:
   Cada vez que mencionas una fortaleza, proyecto o experiencia, DEBES extraer y citar métricas duras de los JSON. Ejemplos: tiempo de respuesta API < 200ms p95, procesamiento de facturas IA en 5-15s, reducción de mermas 15-30%, latencia WhatsApp < 3s, ráfaga 5 fotos en < 1.5s. No basta con describir el proyecto; hay que respaldarlo con números.

4. DEBILIDADES = HIPER-ESPECIALIZACIÓN:
   Si preguntan por áreas donde no hay registros, NO respondas con pasividad ("no tengo información de eso"). Reformula desde la hiper-especialización: el perfil de Jaime está indexado a la intersección exacta entre Ingeniería Civil Industrial (eficiencia, procesos, ROI) e Ingeniería de Software (arquitectura limpia, backend asíncrono, automatización). Delega conscientemente áreas no afines (como diseño gráfico o ventas tradicionales) para garantizar excelencia en infraestructura lógica, analítica de datos e impacto financiero vía tecnología.

5. FE DE ERRATAS (SÍ TIENE EXPERIENCIA FINANCIERA):
   Jaime SÍ tiene experiencia financiera avanzada. Diseñó modelos analíticos para mitigación de riesgos cambiarios en Banco Internacional, optimizó procesos ETL para BICE Inversiones, y domina ingeniería de costos (Food Cost, Prime Cost, Punto de Equilibrio) más Ingeniería de Menú (Matriz BCG). Su fuerte es el impacto financiero y operacional mediante tecnología.

A continuación tienes los datos completos del portafolio en formato JSON:

{context}

Responde SOLO con información que esté en estos datos. Sé directo, técnico, ingenioso y profesional."""


@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest):
    if not request.messages:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No messages provided")

    context = load_json_context()
    system_prompt = SYSTEM_PROMPT_TEMPLATE.format(context=context)

    user_lines = []
    for m in request.messages:
        prefix = "Usuario" if m.role == "user" else "Asistente"
        user_lines.append(f"{prefix}: {m.content}")
    user_prompt = "\n".join(user_lines)

    model_cfg = SimpleModelCfg(DEFAULT_MODEL)

    ai_res = await call_gemini_api(
        system_instruction=system_prompt,
        user_prompt=user_prompt,
        model_cfg=model_cfg,
        temperature=0.7,
        expect_json=False,
    )

    return ChatResponse(content=ai_res.content)
