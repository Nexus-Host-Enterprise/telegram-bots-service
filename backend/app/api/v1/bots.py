from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.schemas.bot import BotCreate, BotRead
from app.models.bot import Bot
from sqlalchemy import insert, select, update, delete
from app.api.v1.users import get_current_user
from app.models.user import User
from app.services.deploy_service import generate_and_prepare_bot
from app.services.bot_manager_client import deploy_bot_request, stop_bot_request
from app.tasks.deploy_tasks import deploy_bot_task
import uuid

deploy_bot_task.delay(bot_id, str(current_user.id), payload.template_name, payload.config or {}, payload.tg_token)
router = APIRouter(prefix="/api/v1/bots", tags=["bots"])

@router.post("", response_model=BotRead)
async def create_bot(payload: BotCreate, background_tasks: BackgroundTasks, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    bot_id = str(uuid.uuid4())
    stmt = insert(Bot).values(
        id=bot_id,
        owner_id=current_user.id,
        name=payload.name,
        template_name=payload.template_name,
        config=payload.config,
        status="creating"
    ).returning(Bot)
    res = await db.execute(stmt)
    await db.commit()

    # schedule background job to generate code and call bot-manager
    async def bg_task():
        try:
            info = await generate_and_prepare_bot(bot_id, str(current_user.id), payload.template_name, payload.config or {}, payload.tg_token)
            # call bot-manager
            resp = await deploy_bot_request(bot_id, info["project_path"], env={})
            await db.execute(update(Bot).where(Bot.id==bot_id).values(status="running"))
            await db.commit()
        except Exception as e:
            await db.execute(update(Bot).where(Bot.id==bot_id).values(status="failed"))
            await db.commit()

    background_tasks.add_task(bg_task)

    q = await db.execute(select(Bot).filter_by(id=bot_id))
    bot = q.scalars().first()
    return bot

@router.get("", response_model=list[BotRead])
async def list_bots(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    q = await db.execute(select(Bot).filter_by(owner_id=current_user.id))
    bots = q.scalars().all()
    return bots

@router.get("/{bot_id}", response_model=BotRead)
async def get_bot(bot_id: str, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    q = await db.execute(select(Bot).filter_by(id=bot_id, owner_id=current_user.id))
    bot = q.scalars().first()
    if not bot:
        raise HTTPException(status_code=404, detail="Bot not found")
    return bot

@router.post("/{bot_id}/stop")
async def stop_bot(bot_id: str, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    q = await db.execute(select(Bot).filter_by(id=bot_id, owner_id=current_user.id))
    bot = q.scalars().first()
    if not bot:
        raise HTTPException(status_code=404, detail="Bot not found")
    await db.execute(update(Bot).where(Bot.id==bot_id).values(status="stopped"))
    await db.commit()
    # call bot-manager
    await stop_bot_request(bot_id)
    return {"status": "stopped"}
