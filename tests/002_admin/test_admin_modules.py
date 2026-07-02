import uuid
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio(loop_scope="session")
async def test_admin_get_all_modules(admin_client: AsyncClient):
    """
    ISO 9001 §9.1 — Visibilidad del catálogo SaaS.
    Listar todos los módulos disponibles.
    Success → El superadmin ve el catálogo completo de módulos SaaS.
    """
    response = await admin_client.get("/admin/modules")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


@pytest.mark.asyncio(loop_scope="session")
async def test_admin_create_module(admin_client: AsyncClient):
    """
    ISO 27001 A.12.1.2, ISO 9001 §8.1 — Creación de módulo SaaS.
    El superadmin crea un nuevo módulo en el catálogo.
    Success → El catálogo de productos SaaS se expande controladamente.
    """
    import uuid
    code = f"mod_{uuid.uuid4().hex[:6]}"
    payload = {
        "code": code,
        "name": "Módulo Test ISO",
        "description": "Módulo creado para pruebas ISO",
        "is_active": True,
    }
    response = await admin_client.post("/admin/modules", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["code"] == code
    assert data["name"] == "Módulo Test ISO"
    assert data["is_active"] is True
    assert "id" in data


@pytest.mark.asyncio(loop_scope="session")
async def test_admin_create_duplicate_module_code_fails(admin_client: AsyncClient, app_module: dict):
    """
    ISO 9001 §8.3 — Unicidad del código de módulo.
    Crear un módulo con código duplicado debe fallar.
    Success → No hay módulos con códigos duplicados (evita colisiones).
    """
    payload = {
        "code": app_module["code"],
        "name": "Módulo Duplicado",
        "is_active": True,
    }
    response = await admin_client.post("/admin/modules", json=payload)

    assert response.status_code in (400, 409), (
        f"Código de módulo duplicado debe fallar, got {response.status_code}"
    )


@pytest.mark.asyncio(loop_scope="session")
async def test_admin_update_module(admin_client: AsyncClient, app_module: dict):
    """
    ISO 27001 A.12.1.2 — Actualización de módulo.
    Cambiar nombre, descripción y estado de un módulo existente.
    Success → La configuración de módulos se actualiza sin interrupción.
    """
    mod_id = app_module["id"]
    payload = {
        "code": app_module["code"],
        "name": "Módulo Actualizado ISO",
        "description": "Descripción actualizada",
        "is_active": False,
    }
    response = await admin_client.put(f"/admin/modules/{mod_id}", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Módulo Actualizado ISO"
    assert data["is_active"] is False

    # Restore
    restore = {
        "code": app_module["code"],
        "name": app_module["name"],
        "description": app_module.get("description"),
        "is_active": True,
    }
    await admin_client.put(f"/admin/modules/{mod_id}", json=restore)


@pytest.mark.asyncio(loop_scope="session")
async def test_admin_update_nonexistent_module_returns_404(admin_client: AsyncClient):
    """
    ISO 9001 §8.3 — Error 404 para módulo inexistente.
    """
    response = await admin_client.put(
        f"/admin/modules/{uuid.uuid4()}",
        json={"code": "no_existe", "name": "No existe"},
    )
    assert response.status_code == 404


@pytest.mark.asyncio(loop_scope="session")
async def test_admin_delete_module(admin_client: AsyncClient, app_module: dict):
    """
    ISO 27001 A.12.6 — Desactivación de módulo.
    Eliminar un módulo del catálogo (el AppModule se borra en cascada).
    """
    import uuid
    code = f"del_mod_{uuid.uuid4().hex[:6]}"
    create = {"code": code, "name": "Módulo a Eliminar", "is_active": True}
    created = await admin_client.post("/admin/modules", json=create)
    mod_id = created.json()["id"]

    delete_resp = await admin_client.delete(f"/admin/modules/{mod_id}")
    assert delete_resp.status_code == 200
    assert delete_resp.json().get("ok") is True

    get_resp = await admin_client.get("/admin/modules")
    all_mods = get_resp.json()
    assert all(m["id"] != str(mod_id) for m in all_mods), (
        "El módulo eliminado no debe aparecer en el catálogo"
    )
