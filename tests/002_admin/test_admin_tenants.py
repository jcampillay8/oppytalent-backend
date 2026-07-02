import uuid
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio(loop_scope="session")
async def test_admin_create_tenant(admin_client: AsyncClient, admin_test_data: dict):
    """
    ISO 27001 A.12.1.2, ISO 9001 §8.5.1 — Aprovisionamiento controlado.
    Crear un Tenant asociado a una Legal Entity.
    Success → Nuevos inquilinos se registran con integridad referencial.
    """
    payload = {
        "schema_name": f"test_tenant_{uuid.uuid4().hex[:6]}",
        "slug": f"test-tenant-{uuid.uuid4().hex[:6]}",
        "nombre_comercial": "Test Tenant ISO",
        "is_active": True,
        "legal_entity_id": str(admin_test_data["legal_entity_id"]),
    }
    response = await admin_client.post("/admin/tenants", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["nombre_comercial"] == "Test Tenant ISO"
    assert data["is_active"] is True
    assert "id" in data


@pytest.mark.asyncio(loop_scope="session")
async def test_admin_get_all_tenants(admin_client: AsyncClient, admin_test_data: dict):
    """
    ISO 9001 §9.1 — Monitoreo de instancias.
    Listar todos los tenants registrados en el sistema.
    Success → El superadmin tiene visibilidad de todos los inquilinos.
    """
    response = await admin_client.get("/admin/tenants")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1

    created = next(
        (t for t in data if t["schema_name"] == "admin_test_schema"), None
    )
    assert created is not None, "El tenant creado en fixtures debe estar en la lista"


@pytest.mark.asyncio(loop_scope="session")
async def test_admin_update_tenant(admin_client: AsyncClient, admin_test_data: dict):
    """
    ISO 27001 A.12.1.2 — Actualización de estado del inquilino.
    Cambiar nombre comercial y estado activo de un tenant.
    Success → Los cambios en inquilinos se reflejan inmediatamente.
    """
    tenant_id = admin_test_data["tenant_id"]
    payload = {
        "schema_name": "admin_test_schema",
        "slug": "admin-test-tenant",
        "nombre_comercial": "Tenant Actualizado ISO",
        "is_active": False,
        "legal_entity_id": str(admin_test_data["legal_entity_id"]),
    }
    response = await admin_client.put(f"/admin/tenants/{tenant_id}", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["nombre_comercial"] == "Tenant Actualizado ISO"
    assert data["is_active"] is False

    # Restore
    restore = {
        "schema_name": "admin_test_schema",
        "slug": "admin-test-tenant",
        "nombre_comercial": "Admin Test Tenant",
        "is_active": True,
        "legal_entity_id": str(admin_test_data["legal_entity_id"]),
    }
    await admin_client.put(f"/admin/tenants/{tenant_id}", json=restore)


@pytest.mark.asyncio(loop_scope="session")
async def test_admin_tenant_slug_uniqueness(admin_client: AsyncClient, admin_test_data: dict):
    """
    ISO 9001 §8.3 — Unicidad de identificadores.
    Verifica que el schema_name (unique en la BD) se respete.
    Success → No pueden existir dos tenants con el mismo schema_name.
    """
    payload = {
        "schema_name": "admin_test_schema",
        "slug": "admin-test-tenant",
        "nombre_comercial": "Tenant Duplicado",
        "is_active": True,
        "legal_entity_id": str(admin_test_data["legal_entity_id"]),
    }
    response = await admin_client.post("/admin/tenants", json=payload)

    assert response.status_code in (400, 409, 500), (
        f"Schema_name duplicado debe fallar, got {response.status_code}"
    )


@pytest.mark.asyncio(loop_scope="session")
async def test_admin_update_nonexistent_tenant_returns_404(admin_client: AsyncClient):
    """
    ISO 9001 §8.3 — Manejo de error 404 consistente para tenants.
    """
    response = await admin_client.put(
        f"/admin/tenants/{uuid.uuid4()}",
        json={
            "schema_name": "no_existe",
            "slug": "no-existe",
            "nombre_comercial": "No existe",
            "legal_entity_id": str(uuid.uuid4()),
        },
    )
    assert response.status_code == 404
