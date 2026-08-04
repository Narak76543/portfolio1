"""Tech stack domain service — ALL DB queries and business logic live here."""

from typing import Any
from src.database import get_supabase_client
from src.tech_stack.constants import STORAGE_BUCKET, TABLE_NAME
from src.tech_stack.exceptions import TechStackNotFound, TechStackUploadFailed
from src.tech_stack.schemas import TechStackCreate, TechStackResponse, TechStackUpdate
from src.tech_stack.utils import _guess_content_type, generate_unique_icon_filename, validate_icon


def _row_to_response(row: dict[str, Any]) -> TechStackResponse:
    """Map DB row to TechStackResponse schema."""
    return TechStackResponse(
        id=row["id"],
        name=row["name"],
        icon_url=row.get("icon_url"),
        display_order=row.get("display_order", 0),
        created_at=row.get("created_at"),
    )


def list_tech_stacks() -> list[TechStackResponse]:
    """Return all tech stack items ordered by display_order ASC."""
    client = get_supabase_client()
    result = (
        client.table(TABLE_NAME)
        .select("*")
        .order("display_order", desc=False)
        .order("created_at", desc=False)
        .execute()
    )
    return [_row_to_response(row) for row in result.data]


def get_tech_stack_by_id(tech_id: str) -> TechStackResponse:
    """Return a single tech stack item by UUID or raise TechStackNotFound."""
    client = get_supabase_client()
    result = (
        client.table(TABLE_NAME)
        .select("*")
        .eq("id", tech_id)
        .execute()
    )
    if not result.data:
        raise TechStackNotFound(tech_id)
    return _row_to_response(result.data[0])


def create_tech_stack(data: TechStackCreate) -> TechStackResponse:
    """Create a new tech stack item."""
    client = get_supabase_client()
    result = (
        client.table(TABLE_NAME)
        .insert(data.model_dump())
        .execute()
    )
    return _row_to_response(result.data[0])


def update_tech_stack(tech_id: str, data: TechStackUpdate) -> TechStackResponse:
    """Update an existing tech stack item."""
    client = get_supabase_client()
    get_tech_stack_by_id(tech_id)

    update_data = data.model_dump(exclude_none=True)
    if not update_data:
        return get_tech_stack_by_id(tech_id)

    result = (
        client.table(TABLE_NAME)
        .update(update_data)
        .eq("id", tech_id)
        .execute()
    )
    return _row_to_response(result.data[0])


def delete_tech_stack(tech_id: str) -> None:
    """Delete a tech stack item by ID."""
    client = get_supabase_client()
    get_tech_stack_by_id(tech_id)
    client.table(TABLE_NAME).delete().eq("id", tech_id).execute()


def upload_icon(file_content: bytes, filename: str) -> str:
    """Upload an icon to Supabase Storage and return the public URL."""
    content_type = _guess_content_type(filename)
    validate_icon(file_content, content_type)

    client = get_supabase_client()
    unique_name = generate_unique_icon_filename(filename)
    path = f"tech-icons/{unique_name}"

    try:
        client.storage.from_(STORAGE_BUCKET).upload(
            path,
            file_content,
            file_options={"content-type": content_type, "upsert": "true"},
        )
    except Exception as exc:
        if "Bucket not found" in str(exc):
            try:
                client.storage.create_bucket(STORAGE_BUCKET, options={"public": True})
                client.storage.from_(STORAGE_BUCKET).upload(
                    path,
                    file_content,
                    file_options={"content-type": content_type, "upsert": "true"},
                )
            except Exception as inner_exc:
                raise TechStackUploadFailed(str(inner_exc)) from inner_exc
        else:
            raise TechStackUploadFailed(str(exc)) from exc

    public_url = client.storage.from_(STORAGE_BUCKET).get_public_url(path)
    return public_url
