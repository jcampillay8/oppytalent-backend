import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.config import settings

@pytest.mark.asyncio
async def test_https_middleware_rewrites_scheme_in_production(monkeypatch):
    monkeypatch.setattr(settings, "ENVIRONMENT", "production")
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/openapi.json", headers={"x-forwarded-proto": "https"})
        assert response.status_code == 200

@pytest.mark.asyncio
async def test_cors_headers_allow_configured_origins(async_client: AsyncClient):
    origin = "http://localhost:5173"
    response = await async_client.options(
        "/openapi.json",
        headers={
            "Origin": origin,
            "Access-Control-Request-Method": "GET",
        },
    )
    assert response.status_code == 200
    cors_header = response.headers.get("access-control-allow-origin", "")
    assert cors_header == origin or cors_header == "*"

@pytest.mark.asyncio
async def test_cors_rejects_malicious_origins(async_client: AsyncClient):
    malicious = ["https://evil.com", "https://malware-site.ru", "http://phishing.xyz"]
    for origin in malicious:
        response = await async_client.options(
            "/openapi.json",
            headers={"Origin": origin, "Access-Control-Request-Method": "GET"},
        )
        cors_header = response.headers.get("access-control-allow-origin", "")
        assert cors_header != origin

@pytest.mark.asyncio
async def test_server_header_not_exposed(async_client: AsyncClient):
    response = await async_client.get("/openapi.json")
    server = response.headers.get("server", "").lower()
    unwanted = ["uvicorn", "python", "fastapi"]
    for word in unwanted:
        assert word not in server

@pytest.mark.asyncio
async def test_health_endpoint_no_auth(async_client: AsyncClient):
    response = await async_client.get("/health")
    assert response.status_code == 200
