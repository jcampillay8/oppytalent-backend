import uuid
import pytest
from httpx import AsyncClient

from src.config import settings


@pytest.mark.asyncio(loop_scope="session")
async def test_admin_create_legal_entity(admin_client: AsyncClient, admin_test_data: dict):
    """
    ISO 27001 A.14.1.1, ISO 9001 §8.2.3 — Validación de datos legales.
    Crear una Legal Entity asociada a un Holding.
    Success → Los datos tributarios se registran con integridad referencial.
    """
    payload = {
        "tax_id": "77.888.999-0",
        "legal_name": "Nueva Entidad Legal ISO",
        "is_active": True,
        "holding_id": str(admin_test_data["holding_id"]),
    }
    response = await admin_client.post("/admin/legal-entities", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["tax_id"] == "77.888.999-0"
    assert data["legal_name"] == "Nueva Entidad Legal ISO"
    assert data["is_active"] is True


@pytest.mark.asyncio(loop_scope="session")
async def test_admin_create_legal_entity_without_holding_fails(
    admin_client: AsyncClient,
):
    """
    ISO 27001 A.14.2, ISO 9001 §8.3 — Integridad referencial.
    Crear Legal Entity sin holding_id debe fallar (violación de FK).
    Success → No se pueden crear entidades legales huérfanas.
    """
    payload = {
        "tax_id": "11.222.333-4",
        "legal_name": "Entidad Huérfana",
        "is_active": True,
        "holding_id": str(uuid.uuid4()),
    }
    response = await admin_client.post("/admin/legal-entities", json=payload)

    assert response.status_code in (400, 500), (
        f"Legal Entity sin holding FK debe fallar, got {response.status_code}"
    )


@pytest.mark.asyncio(loop_scope="session")
async def test_admin_get_all_legal_entities(admin_client: AsyncClient, admin_test_data: dict):
    """
    ISO 9001 §9.1 — Trazabilidad de entidades legales.
    Listar todas las entidades legales con sus tenants anidados.
    Success → El superadmin tiene visibilidad completa de la estructura legal.
    """
    response = await admin_client.get("/admin/legal-entities")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1


@pytest.mark.asyncio(loop_scope="session")
async def test_admin_update_legal_entity(admin_client: AsyncClient, admin_test_data: dict):
    """
    ISO 27001 A.12.1.2 — Actualización controlada.
    Cambiar tax_id, legal_name y estado de una entidad legal.
    Success → Los cambios en datos tributarios se reflejan inmediatamente.
    """
    le_id = admin_test_data["legal_entity_id"]
    payload = {
        "tax_id": "99.888.777-6",
        "legal_name": "Entidad Legal Actualizada ISO",
        "is_active": False,
        "holding_id": str(admin_test_data["holding_id"]),
    }
    response = await admin_client.put(f"/admin/legal-entities/{le_id}", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["tax_id"] == "99.888.777-6"
    assert data["is_active"] is False


@pytest.mark.asyncio(loop_scope="session")
async def test_admin_update_nonexistent_legal_entity_returns_404(
    admin_client: AsyncClient,
):
    """
    ISO 9001 §8.3 — Manejo de error 404 consistente.
    """
    response = await admin_client.put(
        f"/admin/legal-entities/{uuid.uuid4()}",
        json={
            "tax_id": "00.000.000-0",
            "legal_name": "No existe",
            "holding_id": str(uuid.uuid4()),
        },
    )
    assert response.status_code == 404
