import asyncio
from sqlalchemy import update
from app.database import async_session
from app.models.usuario import Usuario

async def test():
    async with async_session() as db:
        await db.execute(update(Usuario).where(Usuario.username.in_(['user01', 'user02'])).values(has_liked_linkedin=True))
        await db.commit()
        print("Updated")
        
asyncio.run(test())
