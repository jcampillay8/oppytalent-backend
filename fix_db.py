import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
import os

DATABASE_URL = "postgresql+asyncpg://neondb_owner:npg_ieMtaqTk74wg@ep-crimson-paper-acrdi7fw-pooler.sa-east-1.aws.neon.tech/portafolio?ssl=require"

async def main():
    engine = create_async_engine(DATABASE_URL)
    async with engine.begin() as conn:
        print("Dropping tables...")
        from sqlalchemy import text
        await conn.execute(text("DROP TABLE IF EXISTS proyecto_traducciones CASCADE;"))
        await conn.execute(text("DROP TABLE IF EXISTS experiencia_traducciones CASCADE;"))
        await conn.execute(text("DROP TABLE IF EXISTS estudio_traducciones CASCADE;"))
        await conn.execute(text("DROP TABLE IF EXISTS perfil_traducciones CASCADE;"))
        await conn.execute(text("DROP TABLE IF EXISTS frase_traducciones CASCADE;"))
        print("Reverting alembic version...")
        await conn.execute(text("UPDATE alembic_version SET version_num = 'c49027744201';"))
        
    await engine.dispose()
    print("Done!")

if __name__ == "__main__":
    asyncio.run(main())
