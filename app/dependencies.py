from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.database import get_db
from app.models.usuario import Usuario

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
) -> Usuario:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.JWT_ACCESS_SECRET_KEY, algorithms=[settings.ENCRYPTION_ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            print("JWT decode failed: sub is None")
            raise credentials_exception
    except JWTError as e:
        print(f"JWTError: {e}")
        raise credentials_exception

    from sqlalchemy import or_
    result = await db.execute(select(Usuario).where(or_(Usuario.username == username, Usuario.email == username)))
    user = result.scalar_one_or_none()
    if user is None:
        print(f"User not found for username/email: {username}")
        raise credentials_exception
    if getattr(user, 'is_deleted', False):
        print(f"User is deleted: {username}")
        raise credentials_exception
    return user


async def get_admin_user(current_user: Usuario = Depends(get_current_user)) -> Usuario:
    if current_user.role != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions. ADMIN role required.",
        )
    return current_user
