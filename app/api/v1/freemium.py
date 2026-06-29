from fastapi import APIRouter, Depends, HTTPException, Request
from typing import Annotated, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select as sa_select
from sqlalchemy import func
from uuid import UUID
from jose import jwt, JWTError

from app.database import get_db
from app.dependencies import get_current_user
from app.models.usuario import Usuario
from app.models.review import Review, ReviewLike
from pydantic import BaseModel
from app.config import settings

router = APIRouter(tags=["Freemium & Social"])

class ReviewCreate(BaseModel):
    content: str
    rating: int

@router.get("/freemium/stats")
async def get_freemium_stats(db_session: Annotated[AsyncSession, Depends(get_db)]):
    from app.models.rbac import Role
    # 1. Total users (Talents)
    users_result = await db_session.execute(
        sa_select(func.count(Usuario.id))
        .join(Role, Usuario.role_id == Role.id)
        .where(Role.name == 'Talent')
        .where(Usuario.email.notlike('%@demo.oppytalent.com%'))
    )
    total_users = users_result.scalar() or 0
    
    # 2. Total reviews
    reviews_result = await db_session.execute(sa_select(func.count(Review.id)))
    total_reviews = reviews_result.scalar() or 0
    
    # 3. Total likes across all reviews + Support Us likes
    likes_result = await db_session.execute(sa_select(func.sum(Review.likes_count)))
    total_review_likes = likes_result.scalar() or 0
    
    support_likes_result = await db_session.execute(sa_select(func.count(Usuario.id)).where(Usuario.has_liked_linkedin == True))
    total_support_likes = support_likes_result.scalar() or 0
    
    total_likes = total_review_likes + total_support_likes
    
    # 4. Total Hunters
    hunters_result = await db_session.execute(
        sa_select(func.count(Usuario.id))
        .join(Role, Usuario.role_id == Role.id)
        .where(Role.name == 'Hunter')
        .where(Usuario.email.notlike('%oppytalent%'))
    )
    total_hunters = hunters_result.scalar() or 0
    
    return {
        "total_talents": total_users,
        "total_reviews": total_reviews,
        "total_likes": int(total_likes),
        "total_hunters": total_hunters
    }

@router.get("/freemium/reviews")
async def get_public_reviews(
    request: Request,
    db_session: Annotated[AsyncSession, Depends(get_db)]
):
    current_user_uuid = None
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]
        try:
            payload = jwt.decode(token, settings.JWT_ACCESS_SECRET_KEY, algorithms=[settings.ENCRYPTION_ALGORITHM])
            username = payload.get("sub")
            if username:
                from sqlalchemy import or_
                result = await db_session.execute(sa_select(Usuario).where(or_(Usuario.custom_slug == username, Usuario.username == username, Usuario.email == username)))
                user = result.scalar_one_or_none()
                if user:
                    current_user_uuid = user.id
        except JWTError:
            pass

    from sqlalchemy.orm import selectinload
    query = sa_select(Review).options(selectinload(Review.author)).order_by(Review.likes_count.desc(), Review.created_at.desc())
    result = await db_session.execute(query)
    reviews = result.scalars().all()
    
    user_likes = set()
    if current_user_uuid:
        likes_query = sa_select(ReviewLike.review_id).where(ReviewLike.usuario_id == current_user_uuid)
        likes_result = await db_session.execute(likes_query)
        user_likes = {str(r) for r in likes_result.scalars().all()}

    output = []
    for r in reviews:
        author = r.author
        from app.models.perfil import Perfil
        # Para el role podemos usar la ocupacion del perfil, si existe, si no un default
        perfil_query = sa_select(Perfil).where(Perfil.usuario_id == author.id)
        perfil_res = await db_session.execute(perfil_query)
        perfil = perfil_res.scalar_one_or_none()
        
        role_str = perfil.ocupacion if perfil and perfil.ocupacion else "Talento OppyTalent"
        
        output.append({
            "id": r.id,
            "author": author.first_name if author.first_name else author.username.split('@')[0],
            "role": role_str,
            "rating": r.rating,
            "content": r.content,
            "likes": r.likes_count,
            "isLiked": str(r.id) in user_likes,
            "date": r.created_at.isoformat()
        })
        
    return output

@router.post("/freemium/reviews")
async def create_review(
    body: ReviewCreate,
    current_user: Annotated[Usuario, Depends(get_current_user)],
    db_session: Annotated[AsyncSession, Depends(get_db)]
):
    # Check if user already reviewed
    existing_query = sa_select(Review).where(Review.usuario_id == current_user.id)
    existing = await db_session.execute(existing_query)
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Ya has escrito una reseña.")
        
    new_review = Review(
        usuario_id=current_user.id,
        content=body.content,
        rating=body.rating
    )
    db_session.add(new_review)
    
    # Misión Cumplida: Subir a Nivel PREMIUM
    if current_user.freemium_tier == "PRO":
        current_user.freemium_tier = "PREMIUM"
        current_user.base_credits_balance = 50
    elif current_user.freemium_tier == "BASIC":
        raise HTTPException(status_code=400, detail="Debes ser nivel PRO antes de desbloquear el plan Premium.")
    
    await db_session.commit()
    return {"status": "success", "message": "¡Reseña publicada! Eres nivel PREMIUM."}

@router.post("/freemium/reviews/{review_id}/like")
async def toggle_like_review(
    review_id: UUID,
    current_user: Annotated[Usuario, Depends(get_current_user)],
    db_session: Annotated[AsyncSession, Depends(get_db)]
):
    review_query = sa_select(Review).where(Review.id == review_id)
    review_res = await db_session.execute(review_query)
    review = review_res.scalar_one_or_none()
    if not review:
        raise HTTPException(status_code=404, detail="Reseña no encontrada")
        
    like_query = sa_select(ReviewLike).where(
        ReviewLike.review_id == review_id,
        ReviewLike.usuario_id == current_user.id
    )
    like_res = await db_session.execute(like_query)
    existing_like = like_res.scalar_one_or_none()
    
    if existing_like:
        # Unlike
        await db_session.delete(existing_like)
        review.likes_count -= 1
        message = "Like eliminado"
    else:
        # Like
        new_like = ReviewLike(review_id=review_id, usuario_id=current_user.id)
        db_session.add(new_like)
        review.likes_count += 1
        message = "¡Like añadido!"
        
        # Misión Cumplida: Subir a Nivel PRO (Solo si es Básico)
        if current_user.freemium_tier == "BASIC":
            current_user.freemium_tier = "PRO"
            current_user.base_credits_balance = 35
            message = "¡Like añadido! Has subido a Nivel PRO."
            
    await db_session.commit()
    return {"status": "success", "message": message, "is_liked": not existing_like, "likes_count": review.likes_count}

@router.post("/freemium/support-us")
async def support_us_upgrade(
    current_user: Annotated[Usuario, Depends(get_current_user)],
    db_session: Annotated[AsyncSession, Depends(get_db)]
):
    current_user.has_liked_linkedin = True
    db_session.add(current_user)
    # Just grant PRO level as a reward for clicking the button
    if current_user.freemium_tier == "BASIC":
        current_user.freemium_tier = "PRO"
        current_user.base_credits_balance = 35
        await db_session.commit()
        return {"status": "success", "message": "¡Has subido a Nivel PRO!"}
    
    await db_session.commit()
    return {"status": "success", "message": "Gracias por tu apoyo."}

@router.get("/freemium/check-referrals")
async def check_referrals(
    current_user: Annotated[Usuario, Depends(get_current_user)],
    db_session: Annotated[AsyncSession, Depends(get_db)]
):
    """
    Returns unread referrals count without clearing.
    """
    unread_count = current_user.unread_referrals_count
    recent_names = []
    
    if unread_count > 0:
        query = sa_select(Usuario).where(Usuario.referred_by_id == current_user.id).order_by(Usuario.created_at.desc()).limit(unread_count)
        result = await db_session.execute(query)
        recent_users = result.scalars().all()
        recent_names = [u.first_name or u.username.split('@')[0] for u in recent_users]

    return {
        "has_unread": unread_count > 0,
        "unread_count": unread_count,
        "bonus_credits": current_user.bonus_credits_balance,
        "freemium_tier": current_user.freemium_tier,
        "recent_names": recent_names
    }

@router.post("/freemium/clear-referrals")
async def clear_referrals(
    current_user: Annotated[Usuario, Depends(get_current_user)],
    db_session: Annotated[AsyncSession, Depends(get_db)]
):
    """
    Clears unread referrals count and returns it.
    """
    unread_count = current_user.unread_referrals_count
    if unread_count > 0:
        current_user.unread_referrals_count = 0
        db_session.add(current_user)
        await db_session.commit()
        
    return {
        "status": "success",
        "cleared_count": unread_count
    }
