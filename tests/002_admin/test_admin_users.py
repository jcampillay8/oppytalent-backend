import pytest
from httpx import AsyncClient


@pytest.mark.asyncio(loop_scope="session")
async def test_admin_get_all_users(admin_client: AsyncClient, admin_test_data: dict):
    """
    ISO 27001 A.9.2.1, ISO 9001 §9.1 — Visibilidad de usuarios.
    El superadmin debe poder listar todos los usuarios del sistema.
    Success → El panel de administración muestra todas las identidades.
    """
    response = await admin_client.get("/admin/users")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    print("ALL USERS:", data)

    superuser = next(
        (u for u in data if u["email"] == "superadmin@oppytest.test"), None
    )
    assert superuser is not None, (
        "El superadmin creado en fixtures debe aparecer en la lista"
    )
    assert superuser.get("is_superuser") in (True,), (
        "El superadmin debe tener is_superuser=True"
    )


@pytest.mark.asyncio(loop_scope="session")
async def test_admin_create_user(admin_client: AsyncClient):
    """
    ISO 27001 A.9.2.1 — Registro controlado de usuarios.
    El superadmin debe poder crear nuevos usuarios desde el panel.
    Success → Nuevas identidades se registran con todos los campos requeridos.
    """
    import uuid
    unique = uuid.uuid4().hex[:6]
    payload = {
        "email": f"newuser.{unique}@test.com",
        "username": f"newuser_{unique}",
        "password": "SecurePass123!",
        "is_active": True,
        "is_superuser": False,
        "role": "user",
    }
    response = await admin_client.post("/admin/users", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["email"] == payload["email"]
    assert data["username"] == payload["username"]
    assert data.get("is_superuser") is False
    assert "id" in data
    # Verify password is never returned
    assert "password" not in data, "La contraseña nunca debe estar en la respuesta"


@pytest.mark.asyncio(loop_scope="session")
async def test_admin_create_user_duplicate_email_fails(admin_client: AsyncClient):
    """
    ISO 9001 §8.3 — Unicidad de email.
    Crear un usuario con email duplicado debe fallar.
    Success → No hay identidades duplicadas en el sistema.
    """
    payload = {
        "email": "superadmin@oppytest.test",
        "username": "duplicate_user",
        "password": "SomePass123!",
        "is_active": True,
    }
    response = await admin_client.post("/admin/users", json=payload)

    assert response.status_code in (400, 409, 500), (
        f"Email duplicado debe fallar, got {response.status_code}"
    )


@pytest.mark.asyncio(loop_scope="session")
async def test_admin_update_user(admin_client: AsyncClient, admin_test_data: dict):
    """
    ISO 27001 A.9.2.3 — Actualización de perfiles por admin.
    El superadmin puede modificar datos de cualquier usuario.
    Success → La gestión de identidades es centralizada y controlada.
    """
    import uuid
    unique = uuid.uuid4().hex[:6]
    unique_email = f"update.user.{unique}@test.com"

    create_payload = {
        "email": unique_email,
        "username": f"update_user_{unique}",
        "password": "InitialPass123!",
        "is_active": True,
    }
    create_resp = await admin_client.post("/admin/users", json=create_payload)
    assert create_resp.status_code == 200
    user_id = create_resp.json()["id"]

    update_payload = {
        "email": unique_email,
        "username": f"updated_user_{unique}",
        "password": "UpdatedPass456!",
        "is_active": False,
    }
    response = await admin_client.put(f"/admin/users/{user_id}", json=update_payload)

    assert response.status_code == 200
    data = response.json()
    assert data["username"] == f"updated_user_{unique}"
    assert data.get("is_active") is False


@pytest.mark.asyncio(loop_scope="session")
async def test_admin_delete_user(admin_client: AsyncClient):
    """
    ISO 27001 A.9.2.1, A.12.6 — Baja de usuarios.
    El superadmin puede eliminar usuarios del sistema.
    Success → La desactivación de identidades es completa y controlada.
    """
    import uuid
    unique = uuid.uuid4().hex[:6]

    create_payload = {
        "email": f"delete.user.{unique}@test.com",
        "username": f"delete_user_{unique}",
        "password": "DeletePass123!",
        "is_active": True,
    }
    create_resp = await admin_client.post("/admin/users", json=create_payload)
    assert create_resp.status_code == 200
    user_id = create_resp.json()["id"]

    delete_resp = await admin_client.delete(f"/admin/users/{user_id}")
    assert delete_resp.status_code == 200
    assert delete_resp.json().get("ok") is True

    get_resp = await admin_client.get("/admin/users")
    all_users = get_resp.json()
    assert all(u["id"] != user_id for u in all_users), (
        "El usuario eliminado no debe aparecer en la lista"
    )


@pytest.mark.asyncio(loop_scope="session")
async def test_admin_delete_nonexistent_user_returns_ok(admin_client: AsyncClient):
    """
    ISO 9001 §8.3 — Idempotencia del borrado.
    Eliminar un usuario que no existe retorna {"ok": True} (comportamiento
    de DELETE idempotente aceptado por REST).
    """
    response = await admin_client.delete("/admin/users/999999")
    assert response.status_code == 200
