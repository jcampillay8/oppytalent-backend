import pytest
from unittest.mock import AsyncMock, patch

@pytest.mark.asyncio
async def test_cache_set_and_get():
    from app.services.cache import set_cached_json, get_cached_json
    with patch("app.services.cache.redis_client.setex", new_callable=AsyncMock) as mock_set:
        mock_set.return_value = True
        await set_cached_json("test:key", {"data": 123}, ttl=60)
        mock_set.assert_called_once()

@pytest.mark.asyncio
async def test_cache_get_returns_none_for_missing():
    from app.services.cache import get_cached_json
    with patch("app.services.cache.redis_client.get", new_callable=AsyncMock) as mock_get:
        mock_get.return_value = None
        result = await get_cached_json("nonexistent:key")
        assert result is None

@pytest.mark.asyncio
async def test_cache_clear_namespace():
    from app.services.cache import clear_cache_namespace
    with patch("app.services.cache.redis_client.keys", new_callable=AsyncMock) as mock_keys:
        mock_keys.return_value = []
        await clear_cache_namespace("test:")
        mock_keys.assert_called_once_with("test::*")

@pytest.mark.asyncio
async def test_redis_rate_limit_client_initialized():
    from app.services.rate_limit import redis_client
    assert redis_client is not None
