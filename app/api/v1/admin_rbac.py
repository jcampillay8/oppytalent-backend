from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from typing import List, Optional
from pydantic import BaseModel

from app.database import get_db
from app.dependencies import RequirePermission
from app.models.usuario import Usuario
from app.models.rbac import Role, Permission, RolePermission

router = APIRouter(prefix="/admin/rbac", tags=["admin-rbac"])

# --- Schemas ---

class PermissionSchema(BaseModel):
    id: UUID
    codename: str
    description: Optional[str]
    
    class Config:
        from_attributes = True

class RoleSchema(BaseModel):
    id: UUID
    name: str
    description: Optional[str]
    permissions: List[PermissionSchema] = []
    
    class Config:
        from_attributes = True

class TogglePermissionSchema(BaseModel):
    permission_id: UUID

class UpdateUserRoleSchema(BaseModel):
    role_id: UUID

class UserWithRoleSchema(BaseModel):
    id: UUID
    username: str
    email: str
    first_name: Optional[str]
    last_name: Optional[str]
    role_id: Optional[int]
    
    class Config:
        from_attributes = True

# --- Endpoints ---

@router.get("/roles", response_model=List[RoleSchema])
async def get_roles(
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(RequirePermission("can_manage_roles"))
):
    """Obtiene la lista de todos los roles y sus permisos asociados."""
    stmt = select(Role).options(selectinload(Role.permissions)).order_by(Role.id)
    result = await db.execute(stmt)
    roles = result.scalars().all()
    return roles

@router.get("/permissions", response_model=List[PermissionSchema])
async def get_permissions(
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(RequirePermission("can_manage_roles"))
):
    """Obtiene la lista de todos los permisos disponibles en el sistema."""
    stmt = select(Permission).order_by(Permission.id)
    result = await db.execute(stmt)
    permissions = result.scalars().all()
    return permissions

@router.post("/roles/{role_id}/permissions/toggle")
async def toggle_role_permission(
    role_id: UUID,
    body: TogglePermissionSchema,
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(RequirePermission("can_manage_roles"))
):
    """
    Agrega o quita un permiso de un rol. 
    Si el rol ya tiene el permiso, se lo quita (Revocar).
    Si el rol no tiene el permiso, se lo agrega (Otorgar).
    """
    # Verificar que el rol existe
    role = await db.get(Role, role_id)
    if not role:
        raise HTTPException(status_code=404, detail="El rol no existe.")
        
    # Verificar que el permiso existe
    permission = await db.get(Permission, body.permission_id)
    if not permission:
        raise HTTPException(status_code=404, detail="El permiso no existe.")
        
    # Verificar si la asociación ya existe
    stmt = select(RolePermission).where(
        RolePermission.role_id == role_id,
        RolePermission.permission_id == body.permission_id
    )
    result = await db.execute(stmt)
    role_permission = result.scalar_one_or_none()
    
    if role_permission:
        # Revocar (Eliminar)
        await db.delete(role_permission)
        action = "revocado"
    else:
        # Otorgar (Agregar)
        new_rp = RolePermission(role_id=role_id, permission_id=body.permission_id)
        db.add(new_rp)
        action = "otorgado"
        
    await db.commit()
    return {"message": f"Permiso '{permission.codename}' {action} para el rol '{role.name}' exitosamente."}

@router.get("/users", response_model=List[UserWithRoleSchema])
async def get_users_with_roles(
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(RequirePermission("can_manage_roles"))
):
    """Obtiene la lista de usuarios para asignarles roles."""
    stmt = select(Usuario).order_by(Usuario.id)
    result = await db.execute(stmt)
    return result.scalars().all()

@router.put("/users/{user_id}/role")
async def update_user_role(
    user_id: UUID,
    body: UpdateUserRoleSchema,
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(RequirePermission("can_manage_roles"))
):
    """Actualiza el rol de un usuario."""
    user = await db.get(Usuario, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")
        
    role = await db.get(Role, body.role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Rol no encontrado.")
        
    user.role_id = role.id
    await db.commit()
    return {"message": f"Rol '{role.name}' asignado al usuario '{user.username}'."}
