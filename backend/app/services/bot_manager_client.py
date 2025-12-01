import httpx
from app.core.config import settings
from typing import Any

async def deploy_bot_request(bot_id: str, project_path: str, env: dict) -> dict:
    async with httpx.AsyncClient(timeout=30) as client:
        url = f"{settings.BOT_MANAGER_URL}/api/v1/deploy"
        payload = {"bot_id": bot_id, "project_path": project_path, "env": env}
        resp = await client.post(url, json=payload)
        resp.raise_for_status()
        return resp.json()

async def stop_bot_request(bot_id: str) -> dict:
    async with httpx.AsyncClient(timeout=10) as client:
        url = f"{settings.BOT_MANAGER_URL}/api/v1/stop"
        resp = await client.post(url, json={"bot_id": bot_id})
        resp.raise_for_status()
        return resp.json()
