import asyncio
from sqlalchemy import select
from app.database import async_session
from app.models.usuario import Usuario

async def test():
    async with async_session() as db:
        res = await db.execute(select(Usuario.email).where(Usuario.has_liked_linkedin == True))
        print("Users with like:", res.scalars().all())
        
asyncio.run(test())
