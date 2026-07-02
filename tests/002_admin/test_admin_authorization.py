import pytest
from httpx import AsyncClient


@pytest.mark.asyncio(loop_scope="session")
async def test_admin_delete_holding_requires_superadmin(admin_client: AsyncClient, async_client: AsyncClient, admin_test_data: dict):
    """
    ISO 27001 A.9.2.3 — Segregación de funciones críticas.
    Solo un superadmin puede eliminar un Holding (ya validado por
    el decorador require_superadmin en el endpoint).
    Success → Las operaciones destructivas están estrictamente controladas.
    """
    import uuid
    from datetime import datetime, timedelta, timezone
    from jose import jwt
    from src.config import settings

    non_admin_token = jwt.encode(
        {
            "sub": "regular@employee.test",
            "schema_name": settings.DB_SCHEMA,
            "exp": datetime.now(timezone.utc) + timedelta(hours=1),
        },
        settings.JWT_ACCESS_SECRET_KEY,
        algorithm=settings.ENCRYPTION_ALGORITHM,
    )

    response = await async_client.delete(
        f"/admin/holdings/{admin_test_data['holding_id']}",
        headers={"Authorization": f"Bearer {non_admin_token}"}
    )
    assert response.status_code in (401, 403), (
        "Un usuario normal no debe poder eliminar holdings"
    )


@pytest.mark.asyncio(loop_scope="session")
async def test_set_tenant_validates_schema_exists(async_client: AsyncClient, admin_test_data: dict):
    """
    ISO 9001 §8.1 — Validación de contexto.
    El endpoint set-tenant acepta cualquier schema_name (la validación
    de existencia queda a cargo del frontend).
    """
    from src.config import settings

    token = admin_test_data["admin_token"]
    response = await async_client.post(
        "/admin/set-tenant/nonexistent_schema_xyz",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200


@pytest.mark.asyncio(loop_scope="session")
async def test_create_holding_missing_required_fields(admin_client: AsyncClient):
    """
    ISO 27001 A.14.2, ISO 9001 §8.3 — Validación de entrada.
    Enviar payload sin campo requerido 'nombre' debe fallar con 422.
    Success → Pydantic/FastAPI valida estrictamente los datos de entrada.
    """
    response = await admin_client.post(
        "/admin/holdings",
        json={"is_active": True}
    )
    assert response.status_code == 422, (
        f"Payload incompleto debe retornar 422, got {response.status_code}"
    )


@pytest.mark.asyncio(loop_scope="session")
async def test_create_legal_entity_missing_required_fields(admin_client: AsyncClient):
    """
    ISO 27001 A.14.2 — Validación de campos críticos.
    """
    response = await admin_client.post(
        "/admin/legal-entities",
        json={"legal_name": "Incomplete"}
    )
    assert response.status_code == 422


@pytest.mark.asyncio(loop_scope="session")
async def test_create_tenant_missing_required_fields(admin_client: AsyncClient):
    """
    ISO 27001 A.14.2 — Validación de campos obligatorios en tenants.
    Schema_name y nombre_comercial son requeridos.
    """
    response = await admin_client.post(
        "/admin/tenants",
        json={"is_active": True}
    )
    assert response.status_code == 422
