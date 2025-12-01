from fastapi import FastAPI
from app.api.v1 import auth, users, templates, bots
from app.db import base  # noqa: F401
from app.db.session import engine
import asyncio

app = FastAPI(title="nexus-bot-platform backend (MVP)")

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(templates.router)
app.include_router(bots.router)

@app.on_event("startup")
async def on_startup():
    # create tables (for MVP only — use Alembic in prod)
    async with engine.begin() as conn:
        await conn.run_sync(base.Base.metadata.create_all)

@app.get("/healthz")
async def healthz():
    return {"status": "ok"}
