
# app/api/v1/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.models.user import User
from app.core.security import verify_password, create_access_token, create_refresh_token, decode_token
from app.schemas.token import Token
from sqlalchemy import select
from datetime import timedelta
from app.services.user_service import create_user_in_db, get_user_by_email, save_refresh_token, revoke_refresh_token

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")

@router.post("/register", response_model=Token)
async def register(payload: dict, db: AsyncSession = Depends(get_db)):
    # payload: {"email":..., "password":..., "full_name":...}
    user = await create_user_in_db(db, payload)
    access = create_access_token(str(user.id))
    refresh = create_refresh_token(str(user.id))
    await save_refresh_token(db, user.id, refresh)
    return {"access_token": access, "token_type": "bearer", "refresh_token": refresh}

@router.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    user = await get_user_by_email(db, form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect credentials")
    access = create_access_token(str(user.id))
    refresh = create_refresh_token(str(user.id))
    await save_refresh_token(db, user.id, refresh)
    return {"access_token": access, "token_type": "bearer", "refresh_token": refresh}

@router.post("/refresh", response_model=Token)
async def refresh_tokens(body: dict, db: AsyncSession = Depends(get_db)):
    # body: {"refresh_token": "..."}
    token = body.get("refresh_token")
    if not token:
        raise HTTPException(status_code=400, detail="Missing refresh token")
    try:
        payload = decode_token(token)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    user_id = payload.get("sub")
    # verify refresh token present in DB
    if not await revoke_refresh_token(db, user_id, token, rotate=False):
        raise HTTPException(status_code=401, detail="Refresh token not recognized")
    # issue new tokens
    new_access = create_access_token(str(user_id))
    new_refresh = create_refresh_token(str(user_id))
    await save_refresh_token(db, user_id, new_refresh)
    return {"access_token": new_access, "token_type": "bearer", "refresh_token": new_refresh}

@router.post("/logout")
async def logout(body: dict, db: AsyncSession = Depends(get_db)):
    token = body.get("refresh_token")
    if token:
        await revoke_refresh_token(db, None, token, rotate=True)
    return {"msg": "ok"}
