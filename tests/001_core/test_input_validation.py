import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_sql_injection_in_query_params(async_client: AsyncClient):
    sql_payloads = [
        "' OR '1'='1",
        "'; DROP TABLE users; --",
        "' UNION SELECT * FROM users; --",
        "1; SELECT pg_sleep(10); --",
        "admin'--",
    ]
    for payload in sql_payloads:
        response = await async_client.get(f"/openapi.json?q={payload}")
        assert response.status_code != 500, f"SQLi payload '{payload}' causó 500"

@pytest.mark.asyncio
async def test_xss_in_request_body(async_client: AsyncClient):
    xss_payloads = [
        {"username": "<script>alert('xss')</script>", "password": "test123"},
        {"username": "<img src=x onerror=alert(1)>", "password": "test123"},
        {"username": "\"><script>alert(1)</script>", "password": "test123"},
    ]
    for payload in xss_payloads:
        response = await async_client.post("/api/v1/auth/login", json=payload)
        assert response.status_code != 500, f"XSS payload causó 500"

@pytest.mark.asyncio
async def test_path_traversal_blocked(async_client: AsyncClient):
    traversal_paths = [
        "/static/../../../etc/passwd",
        "/static/..%2f..%2f..%2fetc%2fpasswd",
        "/static/%2e%2e/%2e%2e/etc/passwd",
    ]
    for path in traversal_paths:
        response = await async_client.get(path)
        assert response.status_code in (401, 403, 404), f"Path traversal '{path}' no bloqueado"

@pytest.mark.asyncio
async def test_oversized_payload_rejected(async_client: AsyncClient):
    large_data = {"data": "x" * 10_000_000}
    response = await async_client.post("/api/v1/auth/login", json=large_data)
    assert response.status_code in (413, 422, 400), f"Payload gigante no rechazado: {response.status_code}"

@pytest.mark.asyncio
async def test_invalid_json_rejected_gracefully(async_client: AsyncClient):
    response = await async_client.post(
        "/api/v1/auth/login",
        content="this is not json at all {{{",
        headers={"Content-Type": "application/json"},
    )
    assert response.status_code in (400, 422)

@pytest.mark.asyncio
async def test_malformed_uuid_rejected(async_client: AsyncClient):
    response = await async_client.get("/api/v1/user/profile/not-a-uuid")
    assert response.status_code in (400, 404, 422)

@pytest.mark.asyncio
async def test_negative_pagination_values(async_client: AsyncClient):
    response = await async_client.get("/api/v1/proyectos/?skip=-1&limit=-10")
    assert response.status_code in (200, 422)
