import asyncio
from passlib.context import CryptContext

# Configurar CryptContext para usar argon2 y bcrypt para compatibilidad legacy
pwd_context = CryptContext(schemes=["argon2", "bcrypt"], deprecated="auto")

async def get_hashed_password(password: str) -> str:
    """Genera un hash seguro para la contraseña usando Argon2."""
    return await asyncio.to_thread(pwd_context.hash, password)

async def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica una contraseña contra su hash."""
    return await asyncio.to_thread(pwd_context.verify, plain_password, hashed_password)

async def needs_rehash(hashed_password: str) -> bool:
    """Verifica si el hash necesita ser actualizado."""
    return await asyncio.to_thread(pwd_context.needs_update, hashed_password)
