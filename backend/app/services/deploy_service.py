import os
import uuid
from app.services.template_engine import render_template
from app.utils.encryption import encrypt_token
from pathlib import Path

BOTS_ROOT = Path("/tmp/nexus_bots")  # change for production

async def generate_and_prepare_bot(bot_id: str, owner_id: str, template_name: str, config: dict, tg_token: str) -> dict:
    # create folder
    bot_dir = BOTS_ROOT / owner_id / bot_id
    bot_dir.mkdir(parents=True, exist_ok=True)

    # render code
    rendered = render_template(template_name, {"config": config})
    code_path = bot_dir / "app.py"
    code_path.write_text(rendered, encoding="utf-8")

    # write env
    encrypted = encrypt_token(tg_token)
    env_path = bot_dir / ".env"
    env_contents = f"TG_TOKEN_ENCRYPTED={encrypted.decode('latin1')}\n"  # store binary as latin1 for simplicity
    env_path.write_text(env_contents, encoding="latin1")

    # Return path and meta
    return {"project_path": str(bot_dir)}
