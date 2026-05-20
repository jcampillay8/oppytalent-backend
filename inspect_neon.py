import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text

async def inspect_db():
    url = "postgresql+asyncpg://neondb_owner:npg_ieMtaqTk74wg@ep-crimson-paper-acrdi7fw-pooler.sa-east-1.aws.neon.tech/portafolio?ssl=require"
    engine = create_async_engine(url, echo=False)
    async with engine.connect() as conn:
        # Get tables
        tables_query = text("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        """)
        result = await conn.execute(tables_query)
        tables = [row[0] for row in result.fetchall()]
        print("TABLES IN NEON:")
        print(tables)
        
        # Check rows
        for t in tables:
            try:
                count_query = text(f"SELECT COUNT(*) FROM {t}")
                count_res = await conn.execute(count_query)
                print(f" - Table {t}: {count_res.scalar()} rows")
            except Exception as e:
                print(f" - Table {t}: Error counting rows: {e}")

asyncio.run(inspect_db())
