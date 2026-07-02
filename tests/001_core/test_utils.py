import pytest
import bcrypt
from app.utils import get_hashed_password, verify_password, needs_rehash

@pytest.mark.asyncio
async def test_password_hashing_argon2id():
    plain = "MySecurePassword123!"
    hashed = await get_hashed_password(plain)
    assert hashed.startswith("$argon2id$")
    assert hashed != plain
    assert await verify_password(plain, hashed) is True
    assert await verify_password("WrongPassword!", hashed) is False

@pytest.mark.asyncio
async def test_legacy_bcrypt_compatibility():
    plain = "LegacyPassword!"
    salt = bcrypt.gensalt()
    legacy_hash = bcrypt.hashpw(plain.encode("utf-8"), salt).decode("utf-8")
    assert await verify_password(plain, legacy_hash) is True
    assert await needs_rehash(legacy_hash) is True

@pytest.mark.asyncio
async def test_argon2_hash_does_not_need_rehash():
    hashed = await get_hashed_password("SecurePass456!")
    assert await needs_rehash(hashed) is False

@pytest.mark.asyncio
async def test_verify_password_rejects_empty():
    hashed = await get_hashed_password("RealPassword")
    assert await verify_password("", hashed) is False
