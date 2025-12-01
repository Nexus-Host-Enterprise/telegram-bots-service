from fastapi import APIRouter, BackgroundTasks, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/api/v1/bot-callback", tags=["bot-callback"])

class CallbackPayload(BaseModel):
    bot_id: str
    status: str
    message: str | None = None

@router.post("")
async def bot_callback(payload: CallbackPayload):
    # validate signature in prod (HMAC/JWT)
    # update Bot.status accordingly (update DB)
    # for brevity, pseudo-code:
    from app.db.session import AsyncSessionLocal
    from sqlalchemy import update
    from app.models.bot import Bot
    async with AsyncSessionLocal() as db:
        await db.execute(update(Bot).where(Bot.id==payload.bot_id).values(status=payload.status))
        await db.commit()
    return {"ok": True}
    