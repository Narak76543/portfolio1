"""Stats domain service — ALL DB queries live here."""

from typing import Any
from src.database import get_supabase_client
from src.stats.constants import TABLE_NAME
from src.stats.exceptions import StatNotFound
from src.stats.schemas import StatCreate, StatResponse, StatUpdate


def _row_to_response(row: dict[str, Any]) -> StatResponse:
    """Map DB row dict to StatResponse schema."""
    return StatResponse(
        id=row["id"],
        label=row["label"],
        value=row["value"],
        icon_name=row.get("icon_name"),
        display_order=row.get("display_order", 0),
        created_at=row.get("created_at"),
    )


def list_stats() -> list[StatResponse]:
    """Return all stat items ordered by display_order ASC."""
    client = get_supabase_client()
    result = (
        client.table(TABLE_NAME)
        .select("*")
        .order("display_order", desc=False)
        .order("created_at", desc=False)
        .execute()
    )
    return [_row_to_response(row) for row in result.data]


def get_stat_by_id(stat_id: str) -> StatResponse:
    """Return a single stat item by ID or raise StatNotFound."""
    client = get_supabase_client()
    result = client.table(TABLE_NAME).select("*").eq("id", stat_id).execute()
    if not result.data:
        raise StatNotFound(stat_id)
    return _row_to_response(result.data[0])


def create_stat(data: StatCreate) -> StatResponse:
    """Create a new stat card item."""
    client = get_supabase_client()
    result = client.table(TABLE_NAME).insert(data.model_dump()).execute()
    return _row_to_response(result.data[0])


def update_stat(stat_id: str, data: StatUpdate) -> StatResponse:
    """Update an existing stat card item."""
    client = get_supabase_client()
    get_stat_by_id(stat_id)

    update_data = data.model_dump(exclude_none=True)
    if not update_data:
        return get_stat_by_id(stat_id)

    result = (
        client.table(TABLE_NAME)
        .update(update_data)
        .eq("id", stat_id)
        .execute()
    )
    return _row_to_response(result.data[0])


def delete_stat(stat_id: str) -> None:
    """Delete a stat card item by ID."""
    client = get_supabase_client()
    get_stat_by_id(stat_id)
    client.table(TABLE_NAME).delete().eq("id", stat_id).execute()
