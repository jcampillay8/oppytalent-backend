from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated, Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select as sa_select

from app.models import Usuario
from app.dependencies import get_current_user
from app.database import get_db

user_details_router = APIRouter(prefix="/user", tags=["Usuario Details"])

@user_details_router.get("/search")
async def search_users(
    q: str,
    db_session: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[Usuario, Depends(get_current_user)],
):
    from sqlalchemy import or_, func
    
    search_term = f"%{q}%"
    query = (
        sa_select(Usuario)
        .where(
            or_(
                Usuario.first_name.ilike(search_term),
                Usuario.last_name.ilike(search_term),
                Usuario.username.ilike(search_term),
                func.concat(Usuario.first_name, ' ', Usuario.last_name).ilike(search_term)
            )
        )
        .limit(20)
    )
    result = await db_session.execute(query)
    users = result.scalars().all()
    
    # Mapeo manual para evitar esquemas complejos heredados
    return [
        {
            "id": u.id,
            "username": u.username,
            "firstName": u.first_name,
            "lastName": u.last_name,
            "userImage": getattr(u, 'avatar_url', None) or getattr(u, 'user_image', None),
            "occupation": "Talento OppyTalent" # Hardcoded temporalmente
        }
        for u in users
    ]

@user_details_router.get("/profile")
async def read_current_user_profile(
    current_user: Annotated[Usuario, Depends(get_current_user)],
):
    # Ya que dependemos de get_current_user, el usuario ya ha sido extraído y validado por token
    return {
        "id": current_user.id,
        "username": current_user.username.split('@')[0],
        "email": current_user.email,
        "firstName": current_user.first_name,
        "lastName": current_user.last_name,
        "userImage": getattr(current_user, 'avatar_url', None) or getattr(current_user, 'user_image', None),
        "occupation": "Talento OppyTalent", # Hardcoded temporalmente
        "roles": [] # Se añadirá si es necesario en un futuro
    }

@user_details_router.get("/{username}")
async def get_user_by_username(
    username: str,
    db_session: Annotated[AsyncSession, Depends(get_db)],
):
    from sqlalchemy import or_
    # Look up by the prefix or full email since usernames are emails right now
    query = sa_select(Usuario).where(
        or_(
            Usuario.username == username,
            Usuario.email == username,
            Usuario.username.ilike(f"{username}@%")
        )
    )
    result = await db_session.execute(query)
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
    return {
        "id": user.id,
        "username": user.username.split('@')[0],
        "firstName": user.first_name,
        "lastName": user.last_name,
        "userImage": getattr(user, 'avatar_url', None) or getattr(user, 'user_image', None),
        "occupation": "Talento OppyTalent",
    }