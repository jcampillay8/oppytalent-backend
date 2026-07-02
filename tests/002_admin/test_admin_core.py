import pytest
from httpx import AsyncClient


@pytest.mark.asyncio(loop_scope="session")
async def test_admin_holdings_requires_auth(async_client: AsyncClient):
    """
    ISO 27001 A.9.2 / A.9.2.3 — Zero Trust.
    Acceso a /admin/holdings sin token DEBE retornar 401.
    Success → Ningún endpoint admin es accesible sin autenticación.
    """
    response = await async_client.get("/admin/holdings")
    assert response.status_code == 401, (
        f"Admin endpoint sin auth debe retornar 401, got {response.status_code}"
    )


@pytest.mark.asyncio(loop_scope="session")
async def test_admin_tenants_requires_auth(async_client: AsyncClient):
    """
    ISO 27001 A.9.2 — Misma protección en todos los endpoints admin.
    """
    response = await async_client.get("/admin/tenants")
    assert response.status_code == 401


@pytest.mark.asyncio(loop_scope="session")
async def test_admin_legal_entities_requires_auth(async_client: AsyncClient):
    response = await async_client.get("/admin/legal-entities")
    assert response.status_code == 401


@pytest.mark.asyncio(loop_scope="session")
async def test_admin_users_requires_auth(async_client: AsyncClient):
    response = await async_client.get("/admin/users")
    assert response.status_code == 401


@pytest.mark.asyncio(loop_scope="session")
async def test_admin_modules_requires_auth(async_client: AsyncClient):
    response = await async_client.get("/admin/modules")
    assert response.status_code == 401


@pytest.mark.asyncio(loop_scope="session")
async def test_admin_business_types_requires_auth(async_client: AsyncClient):
    response = await async_client.get("/admin/business-types")
    assert response.status_code == 401


@pytest.mark.asyncio(loop_scope="session")
async def test_admin_industry_verticals_requires_auth(async_client: AsyncClient):
    response = await async_client.get("/admin/industry-verticals")
    assert response.status_code == 401


@pytest.mark.asyncio(loop_scope="session")
async def test_admin_returns_json_not_html(async_client: AsyncClient):
    """
    ISO 9001 §8.3 — Formato de respuesta consistente.
    Los endpoints admin deben retornar JSON, no HTML.
    """
    response = await async_client.get(
        "/admin/holdings",
        headers={"Authorization": "Bearer invalid_token_xyz"}
    )
    content_type = response.headers.get("content-type", "")
    assert "json" in content_type, (
        f"Admin endpoint debe retornar JSON, got {content_type}"
    )


@pytest.mark.asyncio(loop_scope="session")
async def test_admin_unauthorized_user_gets_403(async_client: AsyncClient):
    """
    ISO 27001 A.9.2.3 — Segregación de funciones.
    Un usuario autenticado pero sin is_superuser debe recibir 403.
    """
    from jose import jwt
    from datetime import datetime, timedelta, timezone
    from src.config import settings

    user_token = jwt.encode(
        {
            "sub": "regular@user.test",
            "schema_name": settings.DB_SCHEMA,
            "exp": datetime.now(timezone.utc) + timedelta(hours=1),
        },
        settings.JWT_ACCESS_SECRET_KEY,
        algorithm=settings.ENCRYPTION_ALGORITHM,
    )

    response = await async_client.get(
        "/admin/holdings",
        headers={"Authorization": f"Bearer {user_token}"}
    )

    assert response.status_code in (401, 403), (
        f"Usuario no superadmin debe recibir 401/403, got {response.status_code}"
    )


@pytest.mark.asyncio(loop_scope="session")
async def test_admin_set_tenant_works(admin_client: AsyncClient):
    """
    ISO 9001 §8.1 — Cambio de contexto de admin.
    El endpoint set-tenant debe funcionar para superadmins.
    """
    response = await admin_client.post(
        "/admin/set-tenant/admin_test_schema"
    )
    assert response.status_code == 200
    data = response.json()
    assert data.get("tenant") == "admin_test_schema"
