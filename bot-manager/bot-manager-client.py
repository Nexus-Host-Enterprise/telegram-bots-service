import httpx
from app.core.config import settings

async def deploy_bot(bot_id: str, project_path: str, env: dict):
    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.post(f"{settings.BOT_MANAGER_URL}/api/v1/deploy", json={
            "bot_id": bot_id,
            "project_path": project_path,
            "env": env
        })
        resp.raise_for_status()
        return resp.json()
