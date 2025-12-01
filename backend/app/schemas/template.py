from pydantic import BaseModel
from typing import Any, Optional

class TemplateRead(BaseModel):
    name: str
    version: str
    description: Optional[str] = None
    config_schema: Optional[dict] = None

    class Config:
        orm_mode = True
