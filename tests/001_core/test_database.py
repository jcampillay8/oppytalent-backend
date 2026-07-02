import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import engine

@pytest.mark.asyncio
async def test_database_engine_pool_configured():
    assert engine.pool is not None
    pool = engine.pool
    assert pool._pool.maxsize >= 5

@pytest.mark.asyncio
async def test_database_url_uses_async_driver():
    from app.config import settings
    url = settings.database_url
    assert url is not None
    assert "asyncpg" in url
    assert url.startswith("postgresql+asyncpg://")

@pytest.mark.asyncio
async def test_database_session_autoflush_disabled(db_session: AsyncSession):
    assert db_session.autoflush is False

@pytest.mark.asyncio
async def test_database_can_execute_raw_sql(db_session: AsyncSession):
    result = await db_session.execute(text("SELECT current_database()"))
    db_name = result.scalar()
    assert db_name is not None
    result = await db_session.execute(text("SELECT current_schema"))
    schema = result.scalar()
    assert schema is not None

@pytest.mark.asyncio
async def test_server_version_postgres(db_session: AsyncSession):
    result = await db_session.execute(text("SHOW server_version"))
    version = result.scalar() or ""
    assert len(version) > 0

@pytest.mark.asyncio
async def test_essential_tables_exist(async_client):
    from app.database import Base
    table_names = list(Base.metadata.tables.keys())
    essential = {"usuarios", "roles", "permissions", "proyectos", "perfiles", "experiencias"}
    found = {t.split(".")[-1] for t in table_names}.intersection(essential)
    assert len(found) > 0, f"Ninguna tabla esencial encontrada en metadata. Tablas: {table_names}"
