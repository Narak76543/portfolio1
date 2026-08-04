"""Profile domain service — ALL business logic and DB queries live here."""

import uuid
from typing import Any

from src.database import get_supabase_client
from src.profile.constants import STORAGE_BUCKET, TABLE_NAME
from src.profile.exceptions import FontUploadFailed, ImageUploadFailed, ProfileNotFound
from src.profile.schemas import ProfileResponse
from src.profile.utils import _guess_content_type, _guess_font_content_type, validate_font, validate_image


def _row_to_response(row: dict[str, Any]) -> ProfileResponse:
    """Map a raw DB row dict to a ProfileResponse schema."""
    return ProfileResponse(
        id=row["id"],
        avatar_url=row.get("avatar_url"),
        tagline=row.get("tagline"),
        about_heading=row.get("about_heading"),
        about_subheading=row.get("about_subheading"),
        about_bio=row.get("about_bio"),
        logo_type=row.get("logo_type", "text"),
        logo_text=row.get("logo_text", "SARAT NARAK"),
        logo_image_url=row.get("logo_image_url"),
        heading_font_url=row.get("heading_font_url"),
        heading_font_name=row.get("heading_font_name"),
        first_name=row.get("first_name", "Sarat"),
        last_name=row.get("last_name", "Narak"),
        hero_pitch=row.get("hero_pitch", "I build backend APIs, mobile apps, and web dashboards — and this site is one of my projects too."),
        updated_at=row.get("updated_at"),
    )


def get_profile() -> ProfileResponse:
    """Return the single profile, or raise ProfileNotFound."""
    client = get_supabase_client()
    result = (
        client.table(TABLE_NAME)
        .select("*")
        .limit(1)
        .execute()
    )
    if not result.data:
        raise ProfileNotFound()
    return _row_to_response(result.data[0])


def update_avatar(file_content: bytes, filename: str) -> ProfileResponse:
    """Upload an image to Supabase Storage and update the profile row."""
    # Validate the image
    content_type = _guess_content_type(filename)
    validate_image(file_content, content_type)

    client = get_supabase_client()
    
    # Check if a profile exists, else create one
    try:
        profile = get_profile()
        profile_id = profile.id
    except ProfileNotFound:
        profile_id = str(uuid.uuid4())
        client.table(TABLE_NAME).insert({"id": profile_id}).execute()

    # Upload to Supabase Storage
    path = f"avatars/saratnarak_{profile_id}.{filename.split('.')[-1] if '.' in filename else 'png'}"
    
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
                raise ImageUploadFailed(str(inner_exc)) from inner_exc
        else:
            raise ImageUploadFailed(str(exc)) from exc
    
    public_url = client.storage.from_(STORAGE_BUCKET).get_public_url(path)
    
    # Update profile row
    result = (
        client.table(TABLE_NAME)
        .update({"avatar_url": public_url})
        .eq("id", profile_id)
        .execute()
    )
    
    return _row_to_response(result.data[0])


def update_profile(data: Any) -> ProfileResponse:
    """Update profile attributes such as tagline, logo settings, and heading font (Admin only)."""
    client = get_supabase_client()
    profile = get_profile()

    update_data = data.model_dump(exclude_unset=True)
    if not update_data:
        return profile

    result = (
        client.table(TABLE_NAME)
        .update(update_data)
        .eq("id", profile.id)
        .execute()
    )
    return _row_to_response(result.data[0])


def upload_logo_image(file_content: bytes, filename: str) -> ProfileResponse:
    """Upload a logo image to Supabase Storage and update profile.logo_image_url."""
    content_type = _guess_content_type(filename)
    validate_image(file_content, content_type)

    client = get_supabase_client()
    profile = get_profile()
    profile_id = profile.id

    path = f"logos/logo_{profile_id}.{filename.split('.')[-1] if '.' in filename else 'png'}"

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
                raise ImageUploadFailed(str(inner_exc)) from inner_exc
        else:
            raise ImageUploadFailed(str(exc)) from exc

    public_url = client.storage.from_(STORAGE_BUCKET).get_public_url(path)

    result = (
        client.table(TABLE_NAME)
        .update({"logo_image_url": public_url, "logo_type": "image"})
        .eq("id", profile_id)
        .execute()
    )

    return _row_to_response(result.data[0])


def upload_heading_font(file_content: bytes, filename: str, font_name: str | None = None) -> ProfileResponse:
    """Upload a custom font file (.woff2, .woff, .ttf) to Supabase Storage and update profile row."""
    validate_font(file_content, filename)
    content_type = _guess_font_content_type(filename)

    client = get_supabase_client()
    profile = get_profile()
    profile_id = profile.id

    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else "ttf"
    path = f"fonts/heading_font_{profile_id}.{ext}"

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
                raise FontUploadFailed(str(inner_exc)) from inner_exc
        else:
            raise FontUploadFailed(str(exc)) from exc

    public_url = client.storage.from_(STORAGE_BUCKET).get_public_url(path)

    derived_font_name = (
        font_name.strip()
        if font_name and font_name.strip()
        else filename.rsplit(".", 1)[0].replace("-", " ").replace("_", " ").title()
    )

    result = (
        client.table(TABLE_NAME)
        .update({
            "heading_font_url": public_url,
            "heading_font_name": derived_font_name,
        })
        .eq("id", profile_id)
        .execute()
    )

    return _row_to_response(result.data[0])


