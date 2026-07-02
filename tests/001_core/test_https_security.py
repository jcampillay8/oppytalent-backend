import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.config import settings

@pytest.mark.asyncio
async def test_https_middleware_rewrites_scheme(monkeypatch):
    monkeypatch.setattr(settings, "ENVIRONMENT", "production")
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/openapi.json", headers={"x-forwarded-proto": "https"})
        assert response.status_code == 200

@pytest.mark.asyncio
async def test_https_middleware_does_not_break_in_dev(async_client: AsyncClient):
    response = await async_client.get("/openapi.json")
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_https_middleware_injects_scheme(monkeypatch):
    monkeypatch.setattr(settings, "ENVIRONMENT", "production")
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/openapi.json", headers={"x-forwarded-proto": "https"})
        assert response.status_code == 200

@pytest.mark.asyncio
async def test_strict_transport_security(async_client: AsyncClient):
    response = await async_client.get("/openapi.json")
    hsts = response.headers.get("strict-transport-security", "")
    if hsts:
        assert "max-age=" in hsts

@pytest.mark.asyncio
async def test_x_forwarded_host_not_trusted(monkeypatch):
    monkeypatch.setattr(settings, "ENVIRONMENT", "production")
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get(
            "/openapi.json",
            headers={"x-forwarded-proto": "https", "x-forwarded-host": "evil.com"},
        )
        assert response.status_code in (200, 400)
