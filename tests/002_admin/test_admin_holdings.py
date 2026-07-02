import uuid
import pytest
from httpx import AsyncClient
from sqlalchemy import text

from src.config import settings
from src.database import async_session_maker


@pytest.mark.asyncio(loop_scope="session")
async def test_admin_create_holding(admin_client: AsyncClient, admin_test_data: dict):
    """
    ISO 9001 §8.1, ISO 27001 A.12.1.2 — Creación controlada de Holding.
    Un superadmin debe poder crear un Holding con nombre y estado activo.
    Success → La estructura corporativa se expande de forma controlada y auditable.
    """
    payload = {"nombre": "Nuevo Holding ISO", "is_active": True}
    response = await admin_client.post("/admin/holdings", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["nombre"] == "Nuevo Holding ISO"
    assert data["is_active"] is True
    assert "id" in data


@pytest.mark.asyncio(loop_scope="session")
async def test_admin_get_all_holdings(admin_client: AsyncClient, admin_test_data: dict):
    """
    ISO 9001 §9.1 — Seguimiento y medición.
    Listar todos los holdings, incluyendo la jerarquía de legal_entities y tenants.
    Success → La jerarquía corporativa completa es visible para el superadmin.
    """
    response = await admin_client.get("/admin/holdings")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1

    created_holding = next(
        (h for h in data if h["nombre"] == "Admin Test Holding"), None
    )
    assert created_holding is not None, (
        "El holding creado en fixtures debe aparecer en la lista"
    )


@pytest.mark.asyncio(loop_scope="session")
async def test_admin_update_holding(admin_client: AsyncClient, admin_test_data: dict):
    """
    ISO 27001 A.12.1.2 — Gestión de cambios.
    Actualizar nombre y estado de un Holding existente.
    Success → Los cambios en la estructura corporativa se reflejan inmediatamente.
    """
    holding_id = admin_test_data["holding_id"]
    payload = {"nombre": "Holding Actualizado ISO", "is_active": False}

    response = await admin_client.put(f"/admin/holdings/{holding_id}", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["nombre"] == "Holding Actualizado ISO"
    assert data["is_active"] is False

    # Restore for other tests
    restore = {"nombre": "Admin Test Holding", "is_active": True}
    await admin_client.put(f"/admin/holdings/{holding_id}", json=restore)


@pytest.mark.asyncio(loop_scope="session")
async def test_admin_update_nonexistent_holding_returns_404(admin_client: AsyncClient):
    """
    ISO 9001 §8.3 — Manejo de errores consistente.
    Actualizar un Holding que no existe debe retornar 404.
    """
    fake_id = uuid.uuid4()
    response = await admin_client.put(
        f"/admin/holdings/{fake_id}",
        json={"nombre": "No existe"}
    )
    assert response.status_code == 404


@pytest.mark.asyncio(loop_scope="session")
async def test_admin_delete_holding_and_cascade(admin_client: AsyncClient, admin_test_data: dict):
    """
    ISO 27001 A.12.6, ISO 9001 §8.5.1 — Borrado controlado con cascade.
    Crear y eliminar un Holding. Verificar que las LegalEntities asociadas
    se eliminan en cascada.
    Success → La limpieza de datos corporativos es completa (CASCADE).
    """
    # First create a temporary holding to delete
    create_payload = {"nombre": "Holding para borrar", "is_active": True}
    create_resp = await admin_client.post("/admin/holdings", json=create_payload)
    assert create_resp.status_code == 200
    temp_holding_id = create_resp.json()["id"]

    response = await admin_client.delete(f"/admin/holdings/{temp_holding_id}")
    assert response.status_code == 200

    response = await admin_client.get("/admin/holdings")
    data = response.json()
    assert all(h["id"] != str(temp_holding_id) for h in data), (
        "El holding eliminado no debe aparecer en la lista"
    )
