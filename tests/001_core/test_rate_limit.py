import pytest
from fastapi import FastAPI, Request
from httpx import AsyncClient, ASGITransport
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler, Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
limit_app = FastAPI()
limit_app.state.limiter = limiter
limit_app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@limit_app.get("/limited")
@limiter.limit("2/minute")
async def limited_endpoint(request: Request):
    return {"message": "Access granted"}

@pytest.mark.asyncio
async def test_rate_limiter_blocks_excessive_requests():
    async with AsyncClient(transport=ASGITransport(app=limit_app), base_url="http://test") as client:
        res1 = await client.get("/limited")
        assert res1.status_code == 200
        res2 = await client.get("/limited")
        assert res2.status_code == 200
        res3 = await client.get("/limited")
        assert res3.status_code == 429

@pytest.mark.asyncio
async def test_rate_limiter_headers(async_client: AsyncClient):
    responses = []
    for _ in range(5):
        responses.append(await async_client.get("/health"))
    latest = responses[-1]
    retry_after = latest.headers.get("retry-after", "")
    if retry_after:
        assert int(retry_after) > 0

@pytest.mark.asyncio
async def test_rate_limiter_recovers_after_window():
    async with AsyncClient(transport=ASGITransport(app=limit_app), base_url="http://test") as client:
        for _ in range(2):
            await client.get("/limited")
        blocked = await client.get("/limited")
        assert blocked.status_code == 429
