"""Skill categories domain dependencies."""

from src.skill_categories import service
from src.skill_categories.schemas import SkillCategoryResponse


def get_skill_category_or_404(category_id: str) -> SkillCategoryResponse:
    """FastAPI dependency to fetch a skill category or raise 404."""
    return service.get_skill_category(category_id)
