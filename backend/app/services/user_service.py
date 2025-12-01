# app/services/user_service.py
from app.models.user import User
from app.models.refresh_token import RefreshToken
from app.core.security import hash_password
from sqlalchemy import select, insert, update
from sqlalchemy.ext.asyncio import AsyncSession

async def create_user_in_db(db: AsyncSession, payload: dict) -> User:
    user = User(email=payload["email"], hashed_password=hash_password(payload["password"]), full_name=payload.get("full_name"))
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    q = await db.execute(select(User).filter_by(email=email))
    return q.scalars().first()

async def save_refresh_token(db: AsyncSession, user_id, token: str):
    rt = RefreshToken(user_id=user_id, token=token)
    db.add(rt)
    await db.commit()

async def revoke_refresh_token(db: AsyncSession, user_id, token: str | None, rotate: bool=False) -> bool:
    if token:
        q = await db.execute(select(RefreshToken).filter_by(token=token, revoked=False))
        rt = q.scalars().first()
        if not rt:
            return False
        rt.revoked = True
        await db.commit()
        return True
    return False
    