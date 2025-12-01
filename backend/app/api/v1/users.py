from fastapi import APIRouter, Depends, HTTPException
from app.schemas.user import UserRead
from app.db.session import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import decode_token
from app.models.user import User
from sqlalchemy import select
from fastapi import Header

router = APIRouter(prefix="/api/v1/users", tags=["users"])

async def get_current_user(authorization: str = Header(...), db: AsyncSession = Depends(get_db)) -> User:
    # Authorization: Bearer <token>
    try:
        scheme, token = authorization.split()
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid auth header")
    payload = decode_token(token)
    sub = payload.get("sub")
    q = await db.execute(select(User).filter_by(id=sub))
    user = q.scalars().first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

@router.get("/me", response_model=UserRead)
async def read_me(current_user: User = Depends(get_current_user)):
    return current_user
