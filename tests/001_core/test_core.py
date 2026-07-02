import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

@pytest.mark.asyncio
async def test_fastapi_starts_and_openapi_is_available(async_client: AsyncClient):
    response = await async_client.get("/openapi.json")
    assert response.status_code == 200
    data = response.json()
    assert "openapi" in data
    assert data["info"]["title"] == "Portafolio API - OppyTalent"

@pytest.mark.asyncio
async def test_health_endpoint(async_client: AsyncClient):
    response = await async_client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

@pytest.mark.asyncio
async def test_database_connection(db_session: AsyncSession):
    result = await db_session.execute(text("SELECT 1"))
    assert result.scalar() == 1

@pytest.mark.asyncio
async def test_openapi_defines_all_routes(async_client: AsyncClient):
    response = await async_client.get("/openapi.json")
    data = response.json()
    paths = data.get("paths", {})
    assert "/health" in paths
    assert "/api/v1/auth/login" in paths
    assert "/api/v1/user/profile" in paths
