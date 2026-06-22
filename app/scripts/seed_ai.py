from app.database import async_session
from app.ai_management.models import AIModelConfig
from app.ai_management.config import GEMINI_PRICING, DEFAULT_MODEL
from sqlalchemy.future import select

async def seed_ai_models():
    """Siembra los modelos de IA por defecto en la base de datos si no existen."""
    async with async_session() as session:
        for model_name, pricing in GEMINI_PRICING.items():
            result = await session.execute(
                select(AIModelConfig).where(AIModelConfig.model_name == model_name)
            )
            config = result.scalar_one_or_none()
            
            if not config:
                new_config = AIModelConfig(
                    model_name=model_name,
                    input_price_per_million=pricing["input_price_per_million"],
                    output_price_per_million=pricing["output_price_per_million"],
                    is_active=True,
                    is_default=(model_name == DEFAULT_MODEL)
                )
                session.add(new_config)
                
        await session.commit()
