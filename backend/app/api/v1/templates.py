from fastapi import APIRouter
from typing import List
from app.schemas.template import TemplateRead

router = APIRouter(prefix="/api/v1/templates", tags=["templates"])

# For MVP - static in-memory list
TEMPLATES = [
    {"name": "faq", "version": "1.0", "description": "FAQ bot", "config_schema": {"questions": "list"}},
    {"name": "feedback", "version": "1.0", "description": "Feedback form", "config_schema": {"fields": "list"}},
]

@router.get("", response_model=List[TemplateRead])
async def list_templates():
    return TEMPLATES
