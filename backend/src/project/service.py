"""Project domain service — ALL business logic and DB queries live here."""

from typing import Any

from src.database import get_supabase_client
from src.project.constants import STORAGE_BUCKET, TABLE_NAME
from src.project.exceptions import ImageUploadFailed, ProjectNotFound, ProjectSlugConflict
from src.project.schemas import ProjectCreate, ProjectResponse, ProjectUpdate
from src.project.utils import generate_unique_filename


def _row_to_response(row: dict[str, Any]) -> ProjectResponse:
    """Map a raw DB row dict to a ProjectResponse schema."""
    return ProjectResponse(
        id=row["id"],
        title=row["title"],
        slug=row["slug"],
        short_description=row.get("short_description"),
        full_description=row.get("full_description"),
        tech_stack=row.get("tech_stack") or [],
        role=row.get("role"),
        github_url=row.get("github_url"),
        live_url=row.get("live_url"),
        cover_image_url=row.get("cover_image_url"),
        featured=row.get("featured", False),
        display_order=row.get("display_order", 0),
        created_at=row["created_at"],
    )


def list_projects() -> list[ProjectResponse]:
    """Return all projects ordered by display_order ASC, then created_at DESC."""
    client = get_supabase_client()
    result = (
        client.table(TABLE_NAME)
        .select("*")
        .order("display_order", desc=False)
        .order("created_at", desc=True)
        .execute()
    )
    return [_row_to_response(row) for row in result.data]


def get_project_by_slug(slug: str) -> ProjectResponse:
    """Return a single project by slug or ID, or raise ProjectNotFound."""
    client = get_supabase_client()
    result = (
        client.table(TABLE_NAME)
        .select("*")
        .eq("slug", slug)
        .execute()
    )
    if not result.data:
        # Fallback to lookup by UUID ID if slug missed
        result = (
            client.table(TABLE_NAME)
            .select("*")
            .eq("id", slug)
            .execute()
        )

    if not result.data:
        raise ProjectNotFound(slug)
    return _row_to_response(result.data[0])


def get_project_by_id(project_id: str) -> ProjectResponse:
    """Return a single project by UUID, or raise ProjectNotFound."""
    client = get_supabase_client()
    result = (
        client.table(TABLE_NAME)
        .select("*")
        .eq("id", project_id)
        .execute()
    )
    if not result.data:
        raise ProjectNotFound(project_id)
    return _row_to_response(result.data[0])


def create_project(data: ProjectCreate) -> ProjectResponse:
    """Insert a new project. Raises ProjectSlugConflict if slug exists."""
    client = get_supabase_client()

    # Check for slug conflict
    existing = (
        client.table(TABLE_NAME)
        .select("id")
        .eq("slug", data.slug)
        .execute()
    )
    if existing.data:
        raise ProjectSlugConflict(data.slug)

    result = (
        client.table(TABLE_NAME)
        .insert(data.model_dump())
        .execute()
    )
    return _row_to_response(result.data[0])


def update_project(project_id: str, data: ProjectUpdate) -> ProjectResponse:
    """Update an existing project. Only non-None fields are updated."""
    client = get_supabase_client()

    # Verify project exists
    get_project_by_id(project_id)

    update_data = data.model_dump(exclude_none=True)

    # Check slug conflict if slug is being changed
    if "slug" in update_data:
        existing = (
            client.table(TABLE_NAME)
            .select("id")
            .eq("slug", update_data["slug"])
            .neq("id", project_id)
            .execute()
        )
        if existing.data:
            raise ProjectSlugConflict(update_data["slug"])

    if not update_data:
        return get_project_by_id(project_id)

    result = (
        client.table(TABLE_NAME)
        .update(update_data)
        .eq("id", project_id)
        .execute()
    )
    return _row_to_response(result.data[0])


def delete_project(project_id: str) -> None:
    """Delete a project by UUID. Raises ProjectNotFound if missing."""
    client = get_supabase_client()

    # Verify project exists
    get_project_by_id(project_id)

    client.table(TABLE_NAME).delete().eq("id", project_id).execute()


def upload_image(file_content: bytes, filename: str) -> str:
    """Upload an image to Supabase Storage and return the public URL."""
    client = get_supabase_client()
    unique_name = generate_unique_filename(filename)
    path = f"covers/{unique_name}"

    try:
        client.storage.from_(STORAGE_BUCKET).upload(
            path,
            file_content,
            file_options={"content-type": _guess_content_type(filename)},
        )
    except Exception as exc:
        if "Bucket not found" in str(exc):
            try:
                client.storage.create_bucket(STORAGE_BUCKET, options={"public": True})
                client.storage.from_(STORAGE_BUCKET).upload(
                    path,
                    file_content,
                    file_options={"content-type": _guess_content_type(filename)},
                )
            except Exception as inner_exc:
                raise ImageUploadFailed(str(inner_exc)) from inner_exc
        else:
            raise ImageUploadFailed(str(exc)) from exc

    public_url = client.storage.from_(STORAGE_BUCKET).get_public_url(path)
    return public_url


def _guess_content_type(filename: str) -> str:
    """Guess the MIME type from a filename extension."""
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    content_types = {
        "jpg": "image/jpeg",
        "jpeg": "image/jpeg",
        "png": "image/png",
        "gif": "image/gif",
        "webp": "image/webp",
        "svg": "image/svg+xml",
    }
    return content_types.get(ext, "application/octet-stream")
