import pytest
from httpx import AsyncClient
from app.config import settings

PUBLIC_ENDPOINTS = ["/health", "/openapi.json", "/api/v1/auth/login"]
PROTECTED_ENDPOINTS = ["/api/v1/user/profile", "/api/v1/admin/rbac/roles"]

@pytest.mark.asyncio
async def test_public_endpoints_accessible_without_auth(async_client: AsyncClient):
    for endpoint in PUBLIC_ENDPOINTS:
        response = await async_client.get(endpoint)
        assert response.status_code in (200, 422, 405), f"{endpoint} no accesible: {response.status_code}"

@pytest.mark.asyncio
async def test_protected_endpoints_reject_unauthorized(async_client: AsyncClient):
    original_headers = dict(async_client.headers)
    async_client.headers.clear()
    for endpoint in PROTECTED_ENDPOINTS:
        response = await async_client.get(endpoint)
        assert response.status_code == 401, f"{endpoint} debió retornar 401, got {response.status_code}"
    async_client.headers.update(original_headers)

@pytest.mark.asyncio
async def test_authenticated_user_can_access_profile(auth_client: AsyncClient):
    response = await auth_client.get("/api/v1/user/profile")
    assert response.status_code == 200
    data = response.json()
    assert "username" in data or "email" in data or "id" in data
