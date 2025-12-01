from app.celery_app import celery
from app.services.deploy_service import generate_and_prepare_bot
from app.services.bot_manager_client import deploy_bot_request
from app.db.session import AsyncSessionLocal
from sqlalchemy.ext.asyncio import AsyncSession
import asyncio
from app.models.bot import Bot
from sqlalchemy import update, select

@celery.task(name="deploy_bot_task")
def deploy_bot_task(bot_id: str, owner_id: str, template_name: str, config: dict, tg_token: str):
    # Celery tasks are sync by default; we can run async io loop when needed
    async def _run():
        async with AsyncSessionLocal() as db:
            try:
                info = await generate_and_prepare_bot(bot_id, owner_id, template_name, config, tg_token)
                # call bot-manager
                await deploy_bot_request(bot_id, info["project_path"], env={})
                await db.execute(update(Bot).where(Bot.id==bot_id).values(status="running"))
                await db.commit()
            except Exception as e:
                await db.execute(update(Bot).where(Bot.id==bot_id).values(status="failed"))
                await db.commit()
    asyncio.run(_run())
    