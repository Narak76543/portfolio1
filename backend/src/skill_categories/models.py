"""Skill categories domain models."""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class SkillCategoryRow:
    """Mirrors the 'skill_categories' table in Supabase/PostgreSQL."""

    id: str
    name: str
    icon_name: str
    items: list[str] = field(default_factory=list)
    display_order: int = 0
    created_at: datetime | None = None
