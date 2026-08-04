"""Social media domain service — ALL DB queries and business logic live here."""

from typing import Any
from src.database import get_supabase_client
from src.social_media.constants import STORAGE_BUCKET, TABLE_NAME
from src.social_media.exceptions import SocialMediaNotFound, SocialMediaUploadFailed
from src.social_media.schemas import SocialMediaCreate, SocialMediaResponse, SocialMediaUpdate
from src.social_media.utils import _guess_content_type, generate_unique_icon_filename, validate_icon


def _row_to_response(row: dict[str, Any]) -> SocialMediaResponse:
    """Map DB row dict to SocialMediaResponse schema."""
    return SocialMediaResponse(
        id=row["id"],
        name=row["name"],
        value=row["value"],
        url=row["url"],
        icon_url=row.get("icon_url"),
        display_order=row.get("display_order", 0),
        created_at=row.get("created_at"),
    )


def list_social_medias() -> list[SocialMediaResponse]:
    """Return all social media items ordered by display_order ASC."""
    client = get_supabase_client()
    result = (
        client.table(TABLE_NAME)
        .select("*")
        .order("display_order", desc=False)
        .order("created_at", desc=False)
        .execute()
    )
    return [_row_to_response(row) for row in result.data]


def get_social_media_by_id(social_id: str) -> SocialMediaResponse:
    """Return a single social media item by ID or raise SocialMediaNotFound."""
    client = get_supabase_client()
    result = client.table(TABLE_NAME).select("*").eq("id", social_id).execute()
    if not result.data:
        raise SocialMediaNotFound(social_id)
    return _row_to_response(result.data[0])


def create_social_media(data: SocialMediaCreate) -> SocialMediaResponse:
    """Create a new social media link item."""
    client = get_supabase_client()
    result = client.table(TABLE_NAME).insert(data.model_dump()).execute()
    return _row_to_response(result.data[0])


def update_social_media(social_id: str, data: SocialMediaUpdate) -> SocialMediaResponse:
    """Update an existing social media item."""
    client = get_supabase_client()
    get_social_media_by_id(social_id)

    update_data = data.model_dump(exclude_none=True)
    if not update_data:
        return get_social_media_by_id(social_id)

    result = (
        client.table(TABLE_NAME)
        .update(update_data)
        .eq("id", social_id)
        .execute()
    )
    return _row_to_response(result.data[0])


def delete_social_media(social_id: str) -> None:
    """Delete a social media item by ID."""
    client = get_supabase_client()
    get_social_media_by_id(social_id)
    client.table(TABLE_NAME).delete().eq("id", social_id).execute()


def upload_icon(file_content: bytes, filename: str) -> str:
    """Upload a social media icon to Supabase Storage and return the public URL."""
    content_type = _guess_content_type(filename)
    validate_icon(file_content, content_type)

    client = get_supabase_client()
    unique_name = generate_unique_icon_filename(filename)
    path = f"social-icons/{unique_name}"

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
                raise SocialMediaUploadFailed(str(inner_exc)) from inner_exc
        else:
            raise SocialMediaUploadFailed(str(exc)) from exc

    public_url = client.storage.from_(STORAGE_BUCKET).get_public_url(path)
    return public_url
