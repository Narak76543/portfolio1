"""Skill categories domain router."""

from fastapi import APIRouter, Depends, status
from src.auth.dependencies import get_current_admin
from src.skill_categories import service
from src.skill_categories.schemas import (
    SkillCategoryCreate,
    SkillCategoryResponse,
    SkillCategoryUpdate,
)

router = APIRouter(prefix="/skill-categories", tags=["skill-categories"])


@router.get("", response_model=list[SkillCategoryResponse])
def list_skill_categories() -> list[SkillCategoryResponse]:
    """Get all skill categories ordered by display_order (Public)."""
    return service.list_skill_categories()


@router.post(
    "",
    response_model=SkillCategoryResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(get_current_admin)],
)
def create_skill_category(data: SkillCategoryCreate) -> SkillCategoryResponse:
    """Create a new skill category (Admin only)."""
    return service.create_skill_category(data)


@router.put(
    "/{category_id}",
    response_model=SkillCategoryResponse,
    dependencies=[Depends(get_current_admin)],
)
def update_skill_category(
    category_id: str, data: SkillCategoryUpdate
) -> SkillCategoryResponse:
    """Update a skill category (Admin only)."""
    return service.update_skill_category(category_id, data)


@router.delete(
    "/{category_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(get_current_admin)],
)
def delete_skill_category(category_id: str) -> None:
    """Delete a skill category (Admin only)."""
    service.delete_skill_category(category_id)
