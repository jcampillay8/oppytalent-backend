import uuid
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio(loop_scope="session")
async def test_admin_get_industry_verticals(admin_client: AsyncClient, industry_vertical: dict):
    """
    ISO 9001 §8.2.3, §9.1 — Catálogo de verticales.
    Listar las verticales de industria disponibles.
    Success → El superadmin puede ver y gestionar las clasificaciones de negocio.
    """
    response = await admin_client.get("/admin/industry-verticals")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert any(iv["nombre"] == "Test Vertical ISO" for iv in data), (
        "La vertical creada en fixtures debe aparecer en la lista"
    )


@pytest.mark.asyncio(loop_scope="session")
async def test_admin_get_business_types(admin_client: AsyncClient):
    """
    ISO 9001 §9.1 — Catálogo de tipos de negocio.
    """
    response = await admin_client.get("/admin/business-types")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


@pytest.mark.asyncio(loop_scope="session")
async def test_admin_create_business_type(admin_client: AsyncClient, industry_vertical: dict):
    """
    ISO 9001 §8.2.3 — Estandarización de tipos de negocio.
    Crear un tipo de negocio asociado a una vertical.
    Success → Los tipos de negocio estandarizan la entrega del software.
    """
    import uuid
    nombre = f"BT_ISO_{uuid.uuid4().hex[:6]}"
    payload = {
        "nombre": nombre,
        "vertical_id": str(industry_vertical["id"]),
        "enabled_modules": {"inventory": True, "sales": False},
        "is_active": True,
    }
    response = await admin_client.post("/admin/business-types", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["nombre"] == nombre
    assert data["vertical"]["nombre"] == "Test Vertical ISO"
    assert data["enabled_modules"] == {"inventory": True, "sales": False}
    assert data["is_active"] is True


@pytest.mark.asyncio(loop_scope="session")
async def test_admin_create_business_type_nonexistent_vertical_fails(
    admin_client: AsyncClient,
):
    """
    ISO 9001 §8.3 — Integridad referencial.
    Crear un BusinessType con vertical_id inexistente debe fallar (FK).
    Success → No hay tipos de negocio huérfanos.
    """
    payload = {
        "nombre": "BT_Huerfano",
        "vertical_id": str(uuid.uuid4()),
        "is_active": True,
    }
    response = await admin_client.post("/admin/business-types", json=payload)

    assert response.status_code in (400, 500), (
        f"BusinessType sin vertical FK debe fallar, got {response.status_code}"
    )


@pytest.mark.asyncio(loop_scope="session")
async def test_admin_update_business_type(admin_client: AsyncClient, industry_vertical: dict):
    """
    ISO 27001 A.12.1.2 — Actualización de clasificación de negocio.
    """
    import uuid
    nombre = f"BT_UPDATE_{uuid.uuid4().hex[:6]}"

    create = await admin_client.post("/admin/business-types", json={
        "nombre": nombre,
        "vertical_id": str(industry_vertical["id"]),
        "enabled_modules": {"inventory": True},
        "is_active": True,
    })
    bt_id = create.json()["id"]

    update = await admin_client.put(f"/admin/business-types/{bt_id}", json={
        "nombre": f"{nombre}_UPDATED",
        "vertical_id": str(industry_vertical["id"]),
        "enabled_modules": {"inventory": True, "sales": True},
        "is_active": False,
    })

    assert update.status_code == 200
    data = update.json()
    assert data["nombre"] == f"{nombre}_UPDATED"
    assert data["is_active"] is False
    assert data["enabled_modules"] == {"inventory": True, "sales": True}


@pytest.mark.asyncio(loop_scope="session")
async def test_admin_delete_business_type(admin_client: AsyncClient, industry_vertical: dict):
    """
    ISO 27001 A.12.6 — Eliminación de tipo de negocio.
    """
    import uuid
    nombre = f"BT_DEL_{uuid.uuid4().hex[:6]}"

    create = await admin_client.post("/admin/business-types", json={
        "nombre": nombre,
        "vertical_id": str(industry_vertical["id"]),
        "is_active": True,
    })
    bt_id = create.json()["id"]

    delete = await admin_client.delete(f"/admin/business-types/{bt_id}")
    assert delete.status_code == 200
    assert delete.json().get("ok") is True

    get = await admin_client.get("/admin/business-types")
    all_bt = get.json()
    assert all(b["id"] != str(bt_id) for b in all_bt)
