"""Skill categories domain service — ALL DB queries & logic live here."""

from typing import Any
from src.database import get_supabase_client
from src.skill_categories.constants import TABLE_NAME
from src.skill_categories.exceptions import SkillCategoryNotFound
from src.skill_categories.schemas import SkillCategoryCreate, SkillCategoryResponse, SkillCategoryUpdate
from src.skill_categories.utils import sanitize_skill_category_items


def _row_to_response(row: dict[str, Any]) -> SkillCategoryResponse:
    """Map a DB row dict to a SkillCategoryResponse schema."""
    return SkillCategoryResponse(
        id=str(row["id"]),
        name=row["name"],
        icon_name=row.get("icon_name", "Folder"),
        items=row.get("items") or [],
        display_order=row.get("display_order", 0),
        created_at=row.get("created_at"),
    )


def list_skill_categories() -> list[SkillCategoryResponse]:
    """Get all skill categories ordered by display_order."""
    client = get_supabase_client()
    result = (
        client.table(TABLE_NAME)
        .select("*")
        .order("display_order", desc=False)
        .execute()
    )
    return [_row_to_response(row) for row in result.data]


def get_skill_category(category_id: str) -> SkillCategoryResponse:
    """Get a single skill category by ID."""
    client = get_supabase_client()
    result = client.table(TABLE_NAME).select("*").eq("id", category_id).execute()
    if not result.data:
        raise SkillCategoryNotFound()
    return _row_to_response(result.data[0])


def create_skill_category(data: SkillCategoryCreate) -> SkillCategoryResponse:
    """Create a new skill category."""
    client = get_supabase_client()
    payload = data.model_dump()
    payload["items"] = sanitize_skill_category_items(payload.get("items", []))

    result = client.table(TABLE_NAME).insert(payload).execute()
    return _row_to_response(result.data[0])


def update_skill_category(category_id: str, data: SkillCategoryUpdate) -> SkillCategoryResponse:
    """Update an existing skill category."""
    client = get_supabase_client()
    _ = get_skill_category(category_id)

    payload = data.model_dump(exclude_unset=True)
    if "items" in payload and payload["items"] is not None:
        payload["items"] = sanitize_skill_category_items(payload["items"])

    if not payload:
        return get_skill_category(category_id)

    result = (
        client.table(TABLE_NAME)
        .update(payload)
        .eq("id", category_id)
        .execute()
    )
    return _row_to_response(result.data[0])


def delete_skill_category(category_id: str) -> None:
    """Delete a skill category."""
    client = get_supabase_client()
    _ = get_skill_category(category_id)
    client.table(TABLE_NAME).delete().eq("id", category_id).execute()
