import os
import re
import pytest
from pathlib import Path
from app.config import settings

REQUIRED_ENV_VARS = [
    "ENVIRONMENT", "JWT_ACCESS_SECRET_KEY", "JWT_REFRESH_SECRET_KEY",
    "ENCRYPTION_ALGORITHM", "database_url", "secret_key",
    "WEBSITE_URL", "API_URL",
]

SECRET_PATTERNS = [
    re.compile(r'(?i)password\s*=\s*["\'][^"\']+["\']'),
    re.compile(r'(?i)api_key\s*=\s*["\'][^"\']+["\']'),
    re.compile(r'(?i)secret\s*=\s*["\'][^"\']{10,}["\']'),
    re.compile(r'(?i)token\s*=\s*["\'][^"\']{10,}["\']'),
]

def _walk_py_files(root_dir):
    root = Path(root_dir)
    py_files = []
    for path in root.rglob("*.py"):
        rel = str(path.relative_to(root))
        if "site-packages" in rel or ".pytest_cache" in rel or "__pycache__" in rel:
            continue
        py_files.append(path)
    return py_files

@pytest.mark.asyncio
async def test_required_env_vars_are_loaded():
    missing = []
    for var_name in REQUIRED_ENV_VARS:
        value = getattr(settings, var_name, None)
        if value is None or (isinstance(value, str) and value.strip() == ""):
            missing.append(var_name)
    assert not missing, f"Variables requeridas faltantes: {missing}"

@pytest.mark.asyncio
async def test_jwt_secret_keys_minimum_length():
    min_len = 32
    for key_name, key_value in [
        ("JWT_ACCESS_SECRET_KEY", settings.JWT_ACCESS_SECRET_KEY),
        ("JWT_REFRESH_SECRET_KEY", settings.JWT_REFRESH_SECRET_KEY),
        ("secret_key", settings.secret_key),
    ]:
        assert len(key_value) >= min_len, f"{key_name} tiene {len(key_value)} chars (mín {min_len})"

@pytest.mark.asyncio
async def test_encryption_algorithm_is_secure():
    allowed = {"HS256", "HS384", "HS512", "RS256", "ES256"}
    assert settings.ENCRYPTION_ALGORITHM in allowed, f"Algoritmo {settings.ENCRYPTION_ALGORITHM} no seguro"

@pytest.mark.asyncio
async def test_database_url_no_env_interpolation():
    url = settings.database_url
    assert url is not None
    assert "$" not in url, f"DATABASE_URL contiene interpolación: {url}"

@pytest.mark.asyncio
async def test_no_hardcoded_secrets_in_source():
    src_dir = os.path.join(os.path.dirname(__file__), "..", "..", "app")
    py_files = _walk_py_files(src_dir)
    violations = []
    for py_file in py_files:
        try:
            content = py_file.read_text(encoding="utf-8")
        except Exception:
            continue
        for pattern in SECRET_PATTERNS:
            matches = pattern.findall(content)
            for match in matches:
                violations.append(f"{py_file}: {match[:60]}")
    assert len(violations) == 0, f"Secretos hardcodeados:\n" + "\n".join(violations[:10])

@pytest.mark.asyncio
async def test_encryption_key_is_set():
    assert settings.ENCRYPTION_KEY is not None, "ENCRYPTION_KEY no está configurada"
    assert len(settings.ENCRYPTION_KEY) >= 10
