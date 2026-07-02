import pytest
from httpx import AsyncClient
from jose import jwt
from datetime import datetime, timedelta, timezone
from app.config import settings

def _make_token(sub="owner@test.com"):
    payload = {
        "sub": sub,
        "exp": datetime.now(timezone.utc) + timedelta(hours=1),
        "iat": datetime.now(timezone.utc),
    }
    return jwt.encode(payload, settings.JWT_ACCESS_SECRET_KEY, algorithm=settings.ENCRYPTION_ALGORITHM)

ADMIN_RBAC_ENDPOINTS = [
    "/api/v1/admin/rbac/roles",
    "/api/v1/admin/rbac/permissions",
    "/api/v1/admin/rbac/users",
]

@pytest.mark.asyncio
async def test_unauthenticated_request_returns_401(async_client: AsyncClient):
    response = await async_client.get("/api/v1/user/profile")
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_public_endpoints_accessible_without_auth(async_client: AsyncClient):
    openapi = await async_client.get("/openapi.json")
    assert openapi.status_code == 200
    health = await async_client.get("/health")
    assert health.status_code == 200

@pytest.mark.asyncio
async def test_admin_rbac_endpoints_require_permission(async_client: AsyncClient, auth_client: AsyncClient):
    for endpoint in ADMIN_RBAC_ENDPOINTS:
        response = await async_client.get(endpoint)
        assert response.status_code == 401, f"{endpoint} sin auth debió ser 401"
    for endpoint in ADMIN_RBAC_ENDPOINTS:
        response = await auth_client.get(endpoint)
        assert response.status_code in (200, 403), f"{endpoint} con auth user debió ser 200/403, got {response.status_code}"

@pytest.mark.asyncio
async def test_admin_rbac_endpoints_accessible_by_admin(admin_auth_client: AsyncClient):
    for endpoint in ADMIN_RBAC_ENDPOINTS:
        response = await admin_auth_client.get(endpoint)
        if response.status_code != 200:
            print(f"FAILED ENDPOINT: {endpoint}, BODY: {response.text}")
        assert response.status_code == 200, f"{endpoint} debió ser accesible por admin, got {response.status_code}"

@pytest.mark.asyncio
async def test_token_with_nonexistent_user_rejected(async_client: AsyncClient):
    token = _make_token(sub="ghost@nowhere.com")
    response = await async_client.get(
        "/api/v1/user/profile",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_authenticated_user_has_role_and_permissions(auth_client: AsyncClient):
    response = await auth_client.get("/api/v1/user/profile")
    assert response.status_code == 200
    data = response.json()
    assert "role" in data or "permissions" in data or "role_id" in data
