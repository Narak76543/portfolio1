"""Skill categories domain pure helper functions."""


def sanitize_skill_category_items(items: list[str]) -> list[str]:
    """Clean and strip empty strings from skill category items."""
    return [item.strip() for item in items if item and item.strip()]
