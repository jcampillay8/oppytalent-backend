from datetime import datetime, timedelta, timezone

from jose import jwt
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.models.usuario import Usuario

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=settings.access_token_expire_minutes)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)


async def authenticate_user(db: AsyncSession, username: str, password: str) -> Usuario | None:
    result = await db.execute(select(Usuario).where(Usuario.username == username))
    user = result.scalar_one_or_none()
    if user is None or not verify_password(password, user.hashed_password):
        return None
    return user


async def seed_admin_user(db: AsyncSession):
    result = await db.execute(
        select(Usuario).where(Usuario.username == settings.admin_username)
    )
    user = result.scalar_one_or_none()
    if not user:
        admin = Usuario(
            username=settings.admin_username,
            email=f"{settings.admin_username}@portafolio.local",
            hashed_password=hash_password(settings.admin_password),
            role="ADMIN",
        )
        db.add(admin)
        await db.flush()
