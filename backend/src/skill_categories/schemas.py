"""Skill categories domain Pydantic schemas."""

from datetime import datetime
from pydantic import BaseModel, ConfigDict


class SkillCategoryCreate(BaseModel):
    name: str
    icon_name: str
    items: list[str] = []
    display_order: int = 0


class SkillCategoryUpdate(BaseModel):
    name: str | None = None
    icon_name: str | None = None
    items: list[str] | None = None
    display_order: int | None = None


class SkillCategoryResponse(BaseModel):
    id: str
    name: str
    icon_name: str
    items: list[str] = []
    display_order: int = 0
    created_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
