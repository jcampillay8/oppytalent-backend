import pytest
import base64
import json
from datetime import datetime, timedelta, timezone
from jose import jwt
from httpx import AsyncClient
from app.config import settings

TENANT_HEADER = {"X-Tenant-Schema": "oppy"}

def _make_token(
    secret=None,
    sub="test@oppytec.com",
    expired=False,
    extra_claims=None,
):
    secret = secret or settings.JWT_ACCESS_SECRET_KEY
    payload = {
        "sub": sub,
        "iat": datetime.now(timezone.utc),
        "exp": (datetime.now(timezone.utc) - timedelta(hours=1)) if expired
               else (datetime.now(timezone.utc) + timedelta(hours=1)),
    }
    if extra_claims:
        payload.update(extra_claims)
    return jwt.encode(payload, secret, algorithm=settings.ENCRYPTION_ALGORITHM)

@pytest.mark.asyncio
async def test_jwt_invalid_secret_rejected(async_client: AsyncClient):
    fake_secret = "this_is_a_completely_different_secret_key_1234567890"
    bad_token = _make_token(secret=fake_secret)
    response = await async_client.get(
        "/api/v1/user/profile",
        headers={"Authorization": f"Bearer {bad_token}", **TENANT_HEADER},
    )
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_expired_jwt_returns_401(async_client: AsyncClient):
    expired_token = _make_token(expired=True)
    response = await async_client.get(
        "/api/v1/user/profile",
        headers={"Authorization": f"Bearer {expired_token}", **TENANT_HEADER},
    )
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_jwt_without_sub_rejected(async_client: AsyncClient):
    token_no_sub = jwt.encode(
        {"exp": datetime.now(timezone.utc) + timedelta(hours=1)},
        settings.JWT_ACCESS_SECRET_KEY,
        algorithm=settings.ENCRYPTION_ALGORITHM,
    )
    response = await async_client.get(
        "/api/v1/user/profile",
        headers={"Authorization": f"Bearer {token_no_sub}", **TENANT_HEADER},
    )
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_tampered_jwt_body_rejected(async_client: AsyncClient):
    valid_token = _make_token()
    parts = valid_token.split(".")
    decoded = json.loads(base64.urlsafe_b64decode(parts[1] + "=="))
    decoded["sub"] = "attacker@evil.com"
    tampered = base64.urlsafe_b64encode(json.dumps(decoded).encode()).decode().rstrip("=")
    tampered_token = f"{parts[0]}.{tampered}.{parts[2]}"
    response = await async_client.get(
        "/api/v1/user/profile",
        headers={"Authorization": f"Bearer {tampered_token}", **TENANT_HEADER},
    )
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_nonexistent_user_in_jwt_rejected(async_client: AsyncClient):
    ghost_token = _make_token(sub="ghost@nonexistent.com")
    response = await async_client.get(
        "/api/v1/user/profile",
        headers={"Authorization": f"Bearer {ghost_token}", **TENANT_HEADER},
    )
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_valid_jwt_grants_access(auth_client: AsyncClient):
    response = await auth_client.get("/api/v1/user/profile")
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_jwt_algorithm_none_rejected(async_client: AsyncClient):
    import base64
    import json
    header = base64.urlsafe_b64encode(b'{"alg":"none","typ":"JWT"}').decode().rstrip("=")
    payload = base64.urlsafe_b64encode(b'{"sub":"test"}').decode().rstrip("=")
    none_token = f"{header}.{payload}."
    response = await async_client.get(
        "/api/v1/user/profile",
        headers={"Authorization": f"Bearer {none_token}", **TENANT_HEADER},
    )
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_jwt_with_empty_token_rejected(async_client: AsyncClient):
    response = await async_client.get(
        "/api/v1/user/profile",
        headers={"Authorization": "Bearer ", **TENANT_HEADER},
    )
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_login_returns_tokens(async_client: AsyncClient, test_user):
    response = await async_client.post(
        "/api/v1/auth/login",
        data={"username": "testuser@oppytalent.com", "password": "TestPass123!"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == 200, f"Error: {response.text}"
    data = response.json()
    assert "access_token" in data or "accessToken" in data
