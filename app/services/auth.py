from datetime import datetime, timedelta, timezone

from jose import jwt
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.models.usuario import Usuario
from app.models.rbac import Role

from app.utils import get_hashed_password, verify_password


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
    if user is None or not await verify_password(password, user.hashed_password):
        return None
    return user


async def seed_admin_user(db: AsyncSession):
    # Buscar el rol Owner (que debió ser creado por seed_rbac)
    role_result = await db.execute(select(Role).where(Role.name == "Owner"))
    owner_role = role_result.scalar_one_or_none()
    role_id = owner_role.id if owner_role else None

    target_username = "jcampillayworks@gmail.com"
    
    result = await db.execute(
        select(Usuario).where(Usuario.username == target_username)
    )
    user = result.scalar_one_or_none()
    
    if not user:
        admin = Usuario(
            username=target_username,
            email=target_username,
            hashed_password=await get_hashed_password(settings.admin_password),
            role="SUPERADMIN",
            role_id=role_id
        )
        db.add(admin)
        await db.flush()
