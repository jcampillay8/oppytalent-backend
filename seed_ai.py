import asyncio
import os
import sys

# Ensure app can be imported
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import async_session
from sqlalchemy import select
from app.ai_management.models import AIModelConfig
from app.models.usuario import Usuario

async def seed():
    async with async_session() as db:
        models = [
            {
                "model_name": "gemini-2.5-flash",
                "input_price_per_million": 0.30,
                "output_price_per_million": 2.50,
                "is_active": True,
                "is_default": False
            },
            {
                "model_name": "gemini-2.5-flash-lite",
                "input_price_per_million": 0.10,
                "output_price_per_million": 0.40,
                "is_active": True,
                "is_default": True
            }
        ]
        
        for cfg_data in models:
            query = select(AIModelConfig).where(AIModelConfig.model_name == cfg_data["model_name"])
            result = await db.execute(query)
            existing = result.scalar_one_or_none()
            
            if not existing:
                new_cfg = AIModelConfig(**cfg_data)
                db.add(new_cfg)
                print(f"Insertado config para {cfg_data['model_name']}")
            else:
                print(f"La configuracion para {cfg_data['model_name']} ya existe.")
                
        await db.commit()
        print("Seed completado con éxito.")

if __name__ == "__main__":
    asyncio.run(seed())
