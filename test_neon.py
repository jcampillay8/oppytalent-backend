import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text

async def test_conn():
    url = "postgresql+asyncpg://neondb_owner:npg_ieMtaqTk74wg@ep-crimson-paper-acrdi7fw-pooler.sa-east-1.aws.neon.tech/portafolio?ssl=require"
    print(f"Connecting to: {url}")
    try:
        engine = create_async_engine(url, echo=True)
        async with engine.begin() as conn:
            result = await conn.execute(text("SELECT 1"))
            print("SUCCESS! Result:", result.scalar())
    except Exception as e:
        print("ERROR CONNECTING TO NEON:")
        import traceback
        traceback.print_exc()

asyncio.run(test_conn())
