import asyncio
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from app.database import async_session
from sqlalchemy import text

async def main():
    async with async_session() as session:
        await session.execute(text("DROP TABLE IF EXISTS oppy.role_permissions CASCADE;"))
        await session.execute(text("DROP TABLE IF EXISTS oppy.permissions CASCADE;"))
        await session.execute(text("DROP TABLE IF EXISTS oppy.roles CASCADE;"))
        await session.execute(text("ALTER TABLE oppy.usuarios DROP COLUMN IF EXISTS role_id;"))
        await session.execute(text("DELETE FROM alembic_version WHERE version_num = 'f9023bf5e76d';"))
        await session.commit()
        print("Dropped")

asyncio.run(main())
