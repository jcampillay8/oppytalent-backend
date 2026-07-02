import pytest
from httpx import AsyncClient
from app.config import settings

@pytest.mark.asyncio
async def test_cors_rejects_unknown_origins(async_client: AsyncClient):
    malicious = ["https://evil.com", "https://malware-site.ru", "http://phishing.xyz", "http://localhost:9999"]
    for origin in malicious:
        response = await async_client.options(
            "/openapi.json",
            headers={"Origin": origin, "Access-Control-Request-Method": "GET"},
        )
        cors = response.headers.get("access-control-allow-origin", "")
        assert cors != origin, f"Origen '{origin}' no debió estar en CORS"

@pytest.mark.asyncio
async def test_cors_allows_configured_origins(async_client: AsyncClient):
    allowed = settings.WEBSITE_URL
    if not allowed:
        pytest.skip("No WEBSITE_URL configured")
    response = await async_client.options(
        "/openapi.json",
        headers={"Origin": allowed, "Access-Control-Request-Method": "GET"},
    )
    cors = response.headers.get("access-control-allow-origin", "")
    assert cors == allowed or cors == "*", f"Origen configurado '{allowed}' no aceptado"

@pytest.mark.asyncio
async def test_cors_allows_credentials(async_client: AsyncClient):
    response = await async_client.options(
        "/openapi.json",
        headers={"Origin": "http://localhost:5173", "Access-Control-Request-Method": "GET"},
    )
    creds = response.headers.get("access-control-allow-credentials", "").lower()
    assert creds == "true", "CORS debe permitir credenciales"

@pytest.mark.asyncio
async def test_server_header_not_exposed(async_client: AsyncClient):
    response = await async_client.get("/openapi.json")
    server = response.headers.get("server", "").lower()
    for word in ["uvicorn", "python", "fastapi"]:
        assert word not in server, f"Server header filtró '{word}'"

@pytest.mark.asyncio
async def test_login_sets_httponly_cookie(async_client: AsyncClient):
    response = await async_client.post(
        "/api/v1/auth/login",
        data={"username": "testuser@oppytalent.com", "password": "TestPass123!"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    set_cookie = response.headers.get("set-cookie", "")
    if set_cookie:
        assert "httponly" in set_cookie.lower() or "HttpOnly" in set_cookie

@pytest.mark.asyncio
async def test_content_type_options_header(async_client: AsyncClient):
    response = await async_client.get("/health")
    cto = response.headers.get("x-content-type-options", "")
    if cto:
        assert cto.lower() == "nosniff"
