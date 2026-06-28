import asyncio
from sqlalchemy import select, func
from app.database import async_session
from app.models.usuario import Usuario

async def test():
    async with async_session() as db:
        res = await db.execute(select(func.count(Usuario.id)))
        print(f"Total: {res.scalar()}")
        
asyncio.run(test())
