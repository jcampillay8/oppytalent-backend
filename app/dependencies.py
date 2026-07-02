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
    except Exception as e:
        print(f"JWTError/Exception: {e}")
        raise credentials_exception

    from sqlalchemy import or_
    result = await db.execute(select(Usuario).where(or_(Usuario.custom_slug == username,
                Usuario.username == username, Usuario.email == username)))
    user = result.scalar_one_or_none()
    if user is None:
        print(f"User not found for username/email: {username}")
        raise credentials_exception
    if getattr(user, 'is_deleted', False):
        print(f"User is deleted: {username}")
        raise credentials_exception
        
    impersonated_role_id = payload.get("impersonated_role_id")
    if impersonated_role_id:
        user.is_impersonating = True
        user.role_id = impersonated_role_id
    else:
        user.is_impersonating = False
        
    return user


async def get_admin_user(current_user: Usuario = Depends(get_current_user)) -> Usuario:
    if current_user.role != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions. ADMIN role required.",
        )
    return current_user

class RequirePermission:
    def __init__(self, codename: str):
        self.codename = codename

    async def __call__(
        self, 
        current_user: Usuario = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
    ) -> Usuario:
        if not current_user.role_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User has no assigned role"
            )
            
        from sqlalchemy import text
        from sqlalchemy.future import select
        from app.models.rbac import Permission, RolePermission
        
        # Check if the role has the requested permission
        query = select(RolePermission).join(
            Permission, RolePermission.permission_id == Permission.id
        ).where(
            RolePermission.role_id == current_user.role_id,
            Permission.codename == self.codename
        )
        
        result = await db.execute(query)
        if not result.first():
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Missing permission: {self.codename}"
            )
            
        return current_user
