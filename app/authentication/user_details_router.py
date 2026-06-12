from app.dependencies import get_tenant_session
# src/authentication/user_details_router.py
from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated, Optional, List
import urllib.parse
import os
import logging
from uuid import UUID

from app.models import Usuario, AppRole
from app.authorization.dependencies import RequirePermission
from app.dependencies import get_current_user, get_tenant_session, require_role
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select as sa_select
from app.authentication.schemas import UsuarioPublicSchema
from pydantic import BaseModel

logger = logging.getLogger(__name__)

user_details_router = APIRouter(prefix="/user", tags=["Usuario Details"])

@user_details_router.get("/profile", response_model=UsuarioPublicSchema, response_model_by_alias=True)
async def read_current_user_profile(
    current_user: Annotated[Usuario, Depends(get_current_user)],
    db_session: Annotated[AsyncSession, Depends(get_tenant_session)],
):
    """
    Retorna el perfil del usuario actual.
    El esquema UsuarioPublicSchema se encarga de inyectar 'show_tour' si no existe.
    """
    from sqlalchemy.orm import selectinload
    query = (
        sa_select(Usuario)
        .options(selectinload(Usuario.areas_operativas))
        .where(Usuario.id == current_user.id)
    )
    result = await db_session.execute(query)
    user_loaded = result.scalar_one()
    
    # Traspasar estado de impersonation si existe
    if getattr(current_user, "is_impersonating", False):
        user_loaded.is_impersonating = True
        user_loaded.is_superuser = False
        user_loaded.roles = current_user.roles
        user_loaded.direct_permissions = []
        
    return user_loaded 

class ProfileUpdateSchema(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    occupation: Optional[str] = None
    user_image: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    areas_operativas_ids: Optional[list[UUID]] = None

class ProfileUpdateResponseSchema(BaseModel):
    user: UsuarioPublicSchema
    requires_approval: bool = False
    pending_fields: List[str] = []

@user_details_router.put("/profile", response_model=ProfileUpdateResponseSchema, response_model_by_alias=True)
async def update_current_user_profile(
    data: ProfileUpdateSchema,
    current_user: Annotated[Usuario, Depends(get_current_user)],
    db_session: Annotated[AsyncSession, Depends(get_tenant_session)],
):
    """Actualiza los datos de perfil del usuario actual, requiriendo aprobación si es usuario estándar."""
    diff = {}
    requires_approval = False
    pending_fields = []

    # Cargo/Role validation
    if data.occupation is not None:
        occupation_lower = data.occupation.lower().strip()
        if "dueño" in occupation_lower or "dueno" in occupation_lower or "owner" in occupation_lower:
            if current_user.role != AppRole.PROPIETARIO:
                raise HTTPException(status_code=400, detail="El cargo 'Dueño' sólo está disponible para propietarios")
        elif "administrador" in occupation_lower or "admin" in occupation_lower:
            if current_user.role not in [AppRole.ADMIN, AppRole.PROPIETARIO]:
                raise HTTPException(status_code=400, detail="El cargo 'Administrador' sólo está disponible para administradores")
        elif "supervisor" in occupation_lower:
            if current_user.role not in [AppRole.SUPERVISOR, AppRole.ADMIN, AppRole.PROPIETARIO]:
                raise HTTPException(status_code=400, detail="El cargo 'Supervisor' sólo está disponible para supervisores, administradores o propietarios")

    # 1. Handle user_image update (always direct, deletes old image if local and replaced)
    if data.user_image is not None and data.user_image != current_user.user_image:
        old_image = current_user.user_image
        current_user.user_image = data.user_image
        if old_image:
            if "/uploads/" in old_image:
                try:
                    filename = old_image.split("/uploads/")[-1]
                    filename = urllib.parse.unquote(filename)
                    filename = os.path.basename(filename)
                    file_path = os.path.join("uploads", filename)
                    if os.path.exists(file_path):
                        os.remove(file_path)
                except Exception as e:
                    logger.error(f"Error removing old avatar file: {e}")

    # 2. Handle text fields
    text_fields = {
        "first_name": "first_name",
        "last_name": "last_name",
        "occupation": "occupation",
        "email": "email",
        "phone": "phone"
    }

    is_standard_user = (current_user.role == AppRole.USER)

    for schema_field, db_field in text_fields.items():
        new_val = getattr(data, schema_field)
        if new_val is not None:
            current_val = getattr(current_user, db_field)
            
            # Check if we should intercept:
            # - Usuario is a standard user AND
            # - The field is currently NOT empty (i.e. is not None and is not empty string after strip) AND
            # - The new value is different from the current value
            is_field_set = current_val is not None and str(current_val).strip() != ""
            is_different = str(new_val).strip() != (str(current_val).strip() if current_val is not None else "")
            
            if is_standard_user and is_field_set and is_different:
                # Intercept change and add to approval request details
                diff[schema_field] = {
                    "old": current_val,
                    "new": new_val
                }
                pending_fields.append(schema_field)
                requires_approval = True
            else:
                # Update directly
                setattr(current_user, db_field, new_val)

    # 3. Handle areas_operativas_ids
    if data.areas_operativas_ids is not None:
        if current_user.role not in [AppRole.ADMIN, AppRole.PROPIETARIO]:
            raise HTTPException(status_code=403, detail="No tienes permisos para modificar tus áreas operativas")
        
        from app.inventory.models import AreaOperativaUsuario
        from sqlalchemy import delete as sa_delete
        
        # Delete old assignments
        await db_session.execute(
            sa_delete(AreaOperativaUsuario).where(
                AreaOperativaUsuario.user_id == current_user.id
            )
        )
        
        # Add new assignments
        for aid in data.areas_operativas_ids:
            db_session.add(AreaOperativaUsuario(area_operativa_id=aid, user_id=current_user.id))

    if requires_approval and diff:
        from app.operations.models import SolicitudAprobacion
        solicitud = SolicitudAprobacion(
            tipo="perfil",
            estado="pendiente",
            usuario_id=current_user.id,
            detalles={"profile_updates": diff}
        )
        db_session.add(solicitud)

    await db_session.commit()
    
    # Reload with areas loaded
    from sqlalchemy.orm import selectinload
    query = (
        sa_select(Usuario)
        .options(selectinload(Usuario.areas_operativas))
        .where(Usuario.id == current_user.id)
    )
    result = await db_session.execute(query)
    user_loaded = result.scalar_one()

    return {
        "user": user_loaded,
        "requires_approval": requires_approval,
        "pending_fields": pending_fields
    }
@user_details_router.post("/accept-terms", status_code=status.HTTP_200_OK)
async def accept_terms(
    current_user: Annotated[Usuario, Depends(get_current_user)],
    db_session: Annotated[AsyncSession, Depends(get_tenant_session)],
):
    """
    Endpoint simple para marcar que el usuario aceptó los términos.
    No crea bots ni chats por ahora.
    """
    if current_user.has_accepted_terms:
        return {"message": "Términos ya aceptados previamente."}

    try:
        current_user.has_accepted_terms = True
        # Solo actualizamos el flag en la base de datos
        await db_session.commit()
        return {"message": "Términos aceptados exitosamente."}
        
    except Exception as e:
        await db_session.rollback()
        logger.error(f"Error al aceptar términos para usuario {current_user.id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno al procesar la solicitud."
        )

# Endpoints obsoletos de merma eliminados

class RoleUpdateSchema(BaseModel):
    role: AppRole

@user_details_router.put("/admin/{user_id}/role", status_code=status.HTTP_200_OK)
async def update_user_role(
    user_id: int,
    data: RoleUpdateSchema,
    current_user: Annotated[Usuario, Depends(RequirePermission("users.manage_profiles"))],
    db_session: Annotated[AsyncSession, Depends(get_tenant_session)],
):
    user = await db_session.get(Usuario, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    # Hierarchy rules:
    # If target is Propietario or Admin, only Propietario can demote them
    if user.role in [AppRole.ADMIN, AppRole.PROPIETARIO] and current_user.role != AppRole.PROPIETARIO:
        raise HTTPException(
            status_code=403,
            detail="Solo el Propietario puede modificar el rol de un Administrador o Propietario"
        )
    
    # If promoting to Owner or Admin, only Owner can do it
    if data.role in [AppRole.PROPIETARIO, AppRole.ADMIN] and current_user.role != AppRole.PROPIETARIO:
        raise HTTPException(
            status_code=403,
            detail="Solo el Propietario puede asignar el rol Administrador o Propietario"
        )

    # 1. Update is_superuser
    user.is_superuser = (data.role == AppRole.PROPIETARIO)
    
    # 2. Update DB roles relationship
    role_map = {
        AppRole.PROPIETARIO: "Propietario",
        AppRole.ADMIN: "Administrador",
        AppRole.SUPERVISOR: "Supervisor",
        AppRole.USER: "Usuario"
    }
    target_role_name = role_map.get(data.role, "Usuario")
    
    from app.authorization.models import Role
    role_query = sa_select(Role).where(Role.name == target_role_name)
    role_db = (await db_session.execute(role_query)).scalar_one_or_none()
    if role_db:
        user.roles = [role_db]
        
    await db_session.commit()
    return {"message": f"Rol actualizado a {data.role.value}"}

@user_details_router.delete("/admin/{user_id}", status_code=status.HTTP_200_OK)
async def delete_user(
    user_id: int,
    current_user: Annotated[Usuario, Depends(RequirePermission("users.manage_profiles"))],
    db_session: Annotated[AsyncSession, Depends(get_tenant_session)],
):
    """Permite al Administrador y Propietario eliminar cualquier usuario, respetando jerarquías."""
    user = await db_session.get(Usuario, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    if user.id == current_user.id:
        raise HTTPException(status_code=400, detail="No puedes eliminarte a ti mismo")

    # Hierarchy check
    if user.role in [AppRole.ADMIN, AppRole.PROPIETARIO] and current_user.role != AppRole.PROPIETARIO:
        raise HTTPException(status_code=403, detail="Solo el Propietario puede eliminar a un Administrador o Propietario")

    await db_session.delete(user)
    await db_session.commit()
    return {"message": "Usuario eliminado exitosamente"}

@user_details_router.post("/admin/{user_id}/merma-permission", status_code=status.HTTP_200_OK)
async def add_merma_permission(
    user_id: int,
    current_admin: Annotated[Usuario, Depends(RequirePermission("users.manage_profiles"))],
    db_session: Annotated[AsyncSession, Depends(get_tenant_session)],
):
    user = await db_session.get(Usuario, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
    from app.authorization.models import Permission
    query = sa_select(Permission).where(Permission.code == "operations.approve_merma")
    result = await db_session.execute(query)
    permission_obj = result.scalar_one_or_none()
    if not permission_obj:
        raise HTTPException(status_code=404, detail="Permiso de merma no registrado en el sistema")
        
    if permission_obj in user.direct_permissions:
        return {"message": "El usuario ya tiene este permiso"}
        
    user.direct_permissions.append(permission_obj)
    await db_session.commit()
    return {"message": "Permiso de merma otorgado"}

@user_details_router.delete("/admin/{user_id}/merma-permission", status_code=status.HTTP_200_OK)
async def remove_merma_permission(
    user_id: int,
    current_admin: Annotated[Usuario, Depends(RequirePermission("users.manage_profiles"))],
    db_session: Annotated[AsyncSession, Depends(get_tenant_session)],
):
    user = await db_session.get(Usuario, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
    from app.authorization.models import Permission
    query = sa_select(Permission).where(Permission.code == "operations.approve_merma")
    result = await db_session.execute(query)
    permission_obj = result.scalar_one_or_none()
    if not permission_obj or permission_obj not in user.direct_permissions:
        return {"message": "El usuario no tenía este permiso"}
        
    user.direct_permissions.remove(permission_obj)
    await db_session.commit()
    return {"message": "Permiso de merma revocado"}

class UsuarioCreateAdminSchema(BaseModel):
    username: str
    email: str
    password: str
    first_name: str
    last_name: str
    occupation: Optional[str] = None
    role: AppRole = AppRole.USER
    areas_operativas_ids: Optional[list[UUID]] = None
    settings: Optional[dict] = None

class UsuarioUpdateAdminSchema(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    occupation: Optional[str] = None
    role: Optional[AppRole] = None
    areas_operativas_ids: Optional[list[UUID]] = None
    settings: Optional[dict] = None

@user_details_router.get("/admin/all", response_model=list[UsuarioPublicSchema], response_model_by_alias=True)
async def get_all_users(
    current_user: Annotated[Usuario, Depends(RequirePermission("users.manage_profiles"))],
    db_session: Annotated[AsyncSession, Depends(get_tenant_session)],
):
    from sqlalchemy.orm import selectinload
    from app.authorization.models import Role
    query = (
        sa_select(Usuario)
        .options(
            selectinload(Usuario.areas_operativas),
            selectinload(Usuario.roles).selectinload(Role.permissions),
            selectinload(Usuario.direct_permissions)
        )
        .order_by(Usuario.id)
    )
    result = await db_session.execute(query)
    return result.scalars().all()


@user_details_router.get("/all", response_model=list[UsuarioPublicSchema], response_model_by_alias=True)
async def get_all_users_public(
    current_user: Annotated[Usuario, Depends(get_current_user)],
    db_session: Annotated[AsyncSession, Depends(get_tenant_session)],
):
    from sqlalchemy.orm import selectinload
    from app.authorization.models import Role
    query = (
        sa_select(Usuario)
        .options(
            selectinload(Usuario.areas_operativas),
            selectinload(Usuario.roles).selectinload(Role.permissions),
            selectinload(Usuario.direct_permissions)
        )
        .order_by(Usuario.id)
    )
    result = await db_session.execute(query)
    users = result.scalars().all()
    
    response_users = []
    for u in users:
        # Mask email and phone if requesting user is AppRole.USER and is not themselves
        if current_user.role == AppRole.USER and u.id != current_user.id:
            u_schema = UsuarioPublicSchema.model_validate(u)
            u_schema.email = "Oculto"
            u_schema.phone = "Oculto"
            response_users.append(u_schema)
        else:
            response_users.append(UsuarioPublicSchema.model_validate(u))
    return response_users

@user_details_router.post("/admin/create", response_model=UsuarioPublicSchema, response_model_by_alias=True)
async def create_user_by_admin(
    data: UsuarioCreateAdminSchema,
    current_user: Annotated[Usuario, Depends(RequirePermission("users.manage_profiles"))],
    db_session: Annotated[AsyncSession, Depends(get_tenant_session)],
):
    # Hierarchy check for role creation
    if data.role in [AppRole.PROPIETARIO, AppRole.ADMIN]:
        if current_user.role != AppRole.PROPIETARIO:
            raise HTTPException(
                status_code=403,
                detail="Solo el Propietario puede crear usuarios con el rol Administrador o Propietario"
            )

    # Cargo validation
    if data.occupation:
        occupation_lower = data.occupation.lower().strip()
        if "dueño" in occupation_lower or "dueno" in occupation_lower or "owner" in occupation_lower:
            if data.role != AppRole.PROPIETARIO:
                raise HTTPException(status_code=400, detail="El cargo 'Dueño' sólo está disponible para el rol Propietario")
        elif "administrador" in occupation_lower or "admin" in occupation_lower:
            if data.role not in [AppRole.ADMIN, AppRole.PROPIETARIO]:
                raise HTTPException(status_code=400, detail="El cargo 'Administrador' sólo está disponible para el rol Administrador o Propietario")
        elif "supervisor" in occupation_lower:
            if data.role not in [AppRole.SUPERVISOR, AppRole.ADMIN, AppRole.PROPIETARIO]:
                raise HTTPException(status_code=400, detail="El cargo 'Supervisor' sólo está disponible para el rol Supervisor, Administrador o Propietario")

    # Uniqueness checks
    exist_username_query = sa_select(Usuario).where(Usuario.username == data.username)
    exist_username = (await db_session.execute(exist_username_query)).scalar_one_or_none()
    if exist_username:
        raise HTTPException(status_code=400, detail="El nombre de usuario ya está registrado")

    exist_email_query = sa_select(Usuario).where(Usuario.email == data.email)
    exist_email = (await db_session.execute(exist_email_query)).scalar_one_or_none()
    if exist_email:
        raise HTTPException(status_code=400, detail="El correo electrónico ya está registrado")

    from app.utils import get_hashed_password
    
    role_map = {
        AppRole.PROPIETARIO: "Propietario",
        AppRole.ADMIN: "Administrador",
        AppRole.SUPERVISOR: "Supervisor",
        AppRole.USER: "Usuario"
    }
    target_role_name = role_map.get(data.role, "Usuario")
    is_super = (target_role_name == "Propietario")

    new_user = Usuario(
        username=data.username,
        email=data.email,
        password=await get_hashed_password(data.password),
        first_name=data.first_name,
        last_name=data.last_name,
        occupation=data.occupation,
        is_superuser=is_super,
        has_completed_onboarding=True,
        has_accepted_terms=True,
        settings=data.settings or {"show_tour": True}
    )
    
    from app.authorization.models import Role
    role_query = sa_select(Role).where(Role.name == target_role_name)
    role_db = (await db_session.execute(role_query)).scalar_one_or_none()
    if role_db:
        new_user.roles = [role_db]

    db_session.add(new_user)
    await db_session.flush()

    if data.areas_operativas_ids:
        from app.inventory.models import AreaOperativaUsuario
        for aid in data.areas_operativas_ids:
            db_session.add(AreaOperativaUsuario(area_operativa_id=aid, user_id=new_user.id))

    await db_session.commit()

    # Reload with areas loaded
    from sqlalchemy.orm import selectinload
    query = (
        sa_select(Usuario)
        .options(selectinload(Usuario.areas_operativas))
        .where(Usuario.id == new_user.id)
    )
    result = await db_session.execute(query)
    return result.scalar_one()

@user_details_router.put("/admin/{user_id}", response_model=UsuarioPublicSchema, response_model_by_alias=True)
async def update_user_by_admin(
    user_id: int,
    data: UsuarioUpdateAdminSchema,
    current_user: Annotated[Usuario, Depends(RequirePermission("users.manage_profiles"))],
    db_session: Annotated[AsyncSession, Depends(get_tenant_session)],
):
    from sqlalchemy.orm import selectinload
    query = (
        sa_select(Usuario)
        .options(selectinload(Usuario.areas_operativas))
        .where(Usuario.id == user_id)
    )
    result = await db_session.execute(query)
    target_user = result.scalar_one_or_none()
    if not target_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Hierarchy rule:
    # If target is Admin or Owner, only Owner (Propietario) can modify them.
    if target_user.role in [AppRole.ADMIN, AppRole.PROPIETARIO]:
        if current_user.role != AppRole.PROPIETARIO:
            raise HTTPException(
                status_code=403,
                detail="Solo el Propietario puede modificar a un Administrador o Propietario"
            )

    # If current user is Admin, they cannot promote anyone to Admin or Owner.
    if data.role is not None and data.role != target_user.role:
        if data.role in [AppRole.ADMIN, AppRole.PROPIETARIO] and current_user.role != AppRole.PROPIETARIO:
            raise HTTPException(
                status_code=403,
                detail="Solo el Propietario puede asignar el rol Administrador o Propietario"
            )

    effective_role = data.role if data.role is not None else target_user.role

    # Cargo validation
    if data.occupation is not None:
        occupation_lower = data.occupation.lower().strip()
        if "dueño" in occupation_lower or "dueno" in occupation_lower or "owner" in occupation_lower:
            if effective_role != AppRole.PROPIETARIO:
                raise HTTPException(status_code=400, detail="El cargo 'Dueño' sólo está disponible para el rol Propietario")
        elif "administrador" in occupation_lower or "admin" in occupation_lower:
            if effective_role not in [AppRole.ADMIN, AppRole.PROPIETARIO]:
                raise HTTPException(status_code=400, detail="El cargo 'Administrador' sólo está disponible para el rol Administrador o Propietario")
        elif "supervisor" in occupation_lower:
            if effective_role not in [AppRole.SUPERVISOR, AppRole.ADMIN, AppRole.PROPIETARIO]:
                raise HTTPException(status_code=400, detail="El cargo 'Supervisor' sólo está disponible para el rol Supervisor, Administrador o Propietario")
    else:
        if target_user.occupation:
            occupation_lower = target_user.occupation.lower().strip()
            if "dueño" in occupation_lower or "dueno" in occupation_lower or "owner" in occupation_lower:
                if effective_role != AppRole.PROPIETARIO:
                    raise HTTPException(status_code=400, detail="El cargo actual 'Dueño' requiere rol Propietario")
            elif "administrador" in occupation_lower or "admin" in occupation_lower:
                if effective_role not in [AppRole.ADMIN, AppRole.PROPIETARIO]:
                    raise HTTPException(status_code=400, detail="El cargo actual 'Administrador' requiere rol Administrador o Propietario")
            elif "supervisor" in occupation_lower:
                if effective_role not in [AppRole.SUPERVISOR, AppRole.ADMIN, AppRole.PROPIETARIO]:
                    raise HTTPException(status_code=400, detail="El cargo actual 'Supervisor' requiere rol Supervisor, Administrador o Propietario")

    if data.first_name is not None:
        target_user.first_name = data.first_name
    if data.last_name is not None:
        target_user.last_name = data.last_name
    if data.email is not None:
        if data.email != target_user.email:
            exist_email_query = sa_select(Usuario).where(Usuario.email == data.email)
            exist_email = (await db_session.execute(exist_email_query)).scalar_one_or_none()
            if exist_email:
                raise HTTPException(status_code=400, detail="El correo electrónico ya está registrado")
        target_user.email = data.email
    if data.phone is not None:
        target_user.phone = data.phone
    if data.occupation is not None:
        target_user.occupation = data.occupation
    if data.role is not None:
        role_map = {
            AppRole.PROPIETARIO: "Propietario",
            AppRole.ADMIN: "Administrador",
            AppRole.SUPERVISOR: "Supervisor",
            AppRole.USER: "Usuario"
        }
        target_role_name = role_map.get(data.role, "Usuario")
        target_user.is_superuser = (target_role_name == "Propietario")
        
        from app.authorization.models import Role
        role_query = sa_select(Role).where(Role.name == target_role_name)
        role_db = (await db_session.execute(role_query)).scalar_one_or_none()
        if role_db:
            target_user.roles = [role_db]

    if data.areas_operativas_ids is not None:
        from app.inventory.models import AreaOperativaUsuario
        from sqlalchemy import delete as sa_delete

        await db_session.execute(
            sa_delete(AreaOperativaUsuario).where(AreaOperativaUsuario.user_id == target_user.id)
        )
        for aid in data.areas_operativas_ids:
            db_session.add(AreaOperativaUsuario(area_operativa_id=aid, user_id=target_user.id))

    if data.settings is not None:
        target_user.settings = {**(target_user.settings or {}), **data.settings}
        from sqlalchemy.orm.attributes import flag_modified
        flag_modified(target_user, "settings")

    await db_session.commit()

    # Reload target user to return updated relations
    query = (
        sa_select(Usuario)
        .options(selectinload(Usuario.areas_operativas))
        .where(Usuario.id == target_user.id)
    )
    result = await db_session.execute(query)
    return result.scalar_one()