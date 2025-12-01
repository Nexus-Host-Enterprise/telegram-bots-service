# bot_manager_stub/botmanager_stub.py
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class DeployPayload(BaseModel):
    bot_id: str
    project_path: str
    env: dict

@app.post("/api/v1/deploy")
async def deploy(payload: DeployPayload):
    # simple stub: pretend deploy succeeded
    print(f"[bot-manager] deploy requested: {payload.bot_id} at {payload.project_path}")
    return {"status": "deployed", "bot_id": payload.bot_id}

@app.post("/api/v1/stop")
async def stop(payload: dict):
    print(f"[bot-manager] stop requested: {payload.get('bot_id')}")
    return {"status": "stopped"}
