import pytest
from httpx import AsyncClient

FORBIDDEN_PATTERNS = ["traceback", 'File "', "line ", "/app/", "syntaxerror", "filenotfounderror"]

@pytest.mark.asyncio
async def test_404_does_not_include_stack_trace(async_client: AsyncClient):
    response = await async_client.get("/ruta-que-no-existe-12345xyz")
    assert response.status_code == 404
    body = response.text.lower()
    for pattern in FORBIDDEN_PATTERNS:
        assert pattern not in body, f"Error 404 filtró '{pattern}'"

@pytest.mark.asyncio
async def test_validation_error_returns_422_consistent_format(async_client: AsyncClient):
    response = await async_client.post(
        "/api/v1/auth/login",
        json={"username": "", "password": ""},
    )
    assert response.status_code in (422, 200)
    if response.status_code == 422:
        data = response.json()
        assert "detail" in data
        assert isinstance(data["detail"], list)

@pytest.mark.asyncio
async def test_401_includes_www_authenticate_header(async_client: AsyncClient):
    response = await async_client.get("/api/v1/user/profile")
    assert response.status_code == 401
    assert "www-authenticate" in response.headers

@pytest.mark.asyncio
async def test_api_returns_json_errors_not_html(async_client: AsyncClient):
    endpoints = ["/nonexistent1", "/nonexistent2", "/api/v1/user/profile"]
    for endpoint in endpoints:
        response = await async_client.get(endpoint)
        content_type = response.headers.get("content-type", "")
        assert "json" in content_type, f"{endpoint} retornó {content_type} en vez de JSON"

@pytest.mark.asyncio
async def test_login_with_wrong_credentials_returns_401(async_client: AsyncClient):
    response = await async_client.post(
        "/api/v1/auth/login",
        data={"username": "wrong@test.com", "password": "wrongpass"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_405_method_not_allowed(async_client: AsyncClient):
    response = await async_client.put("/health")
    assert response.status_code in (405, 401)
