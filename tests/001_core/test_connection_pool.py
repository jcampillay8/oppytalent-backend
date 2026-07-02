import pytest
from app.database import engine

@pytest.mark.asyncio
async def test_database_engine_has_pool():
    assert engine.pool is not None

@pytest.mark.asyncio
async def test_database_pool_maxsize():
    pool = engine.pool
    assert pool._pool.maxsize >= 5

@pytest.mark.asyncio
async def test_database_url_async_driver():
    from app.config import settings
    assert "asyncpg" in settings.database_url

@pytest.mark.asyncio
async def test_database_session_is_async():
    from app.database import async_session
    assert async_session is not None

@pytest.mark.asyncio
async def test_engine_echo_disabled_in_production():
    from app.config import settings
    if settings.ENVIRONMENT == "production":
        from app.database import engine
        assert engine.echo is False
