import os
import pytest
from app.config import settings

@pytest.mark.asyncio
async def test_settings_environment_is_set():
    assert settings.ENVIRONMENT in ("development", "test", "production")

@pytest.mark.asyncio
async def test_settings_database_url_is_postgres_async():
    assert settings.database_url.startswith("postgresql+asyncpg://")

@pytest.mark.asyncio
async def test_settings_redis_url_is_redis():
    assert "redis://" in settings.redis_url

@pytest.mark.asyncio
async def test_settings_jwt_secrets_not_default():
    assert settings.JWT_ACCESS_SECRET_KEY != "super-secret-access"
    assert settings.JWT_REFRESH_SECRET_KEY != "super-secret-refresh"

@pytest.mark.asyncio
async def test_settings_has_encryption_key():
    assert settings.ENCRYPTION_KEY is not None

@pytest.mark.asyncio
async def test_settings_website_url_set():
    assert settings.WEBSITE_URL is not None
    assert len(settings.WEBSITE_URL) > 0

@pytest.mark.asyncio
async def test_settings_google_oauth_configured():
    assert settings.GOOGLE_CLIENT_ID is not None or settings.GOOGLE_CLIENT_SECRET is not None

@pytest.mark.asyncio
async def test_settings_token_expire_reasonable():
    assert settings.ACCESS_TOKEN_EXPIRE_MINUTES > 0
    assert settings.REFRESH_TOKEN_EXPIRE_MINUTES > 0
    assert settings.ACCESS_TOKEN_EXPIRE_MINUTES <= settings.REFRESH_TOKEN_EXPIRE_MINUTES
