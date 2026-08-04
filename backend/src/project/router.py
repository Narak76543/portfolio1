"""Project domain router — HTTP layer only, no DB queries or business logic."""

from fastapi import APIRouter, Depends, UploadFile

from src.auth.schemas import AdminUser
from src.project.dependencies import require_admin
from src.project.schemas import (
    ImageUploadResponse,
    ProjectCreate,
    ProjectResponse,
    ProjectUpdate,
)
from src.project.service import (
    create_project,
    delete_project,
    get_project_by_slug,
    list_projects,
    update_project,
    upload_image,
)

router = APIRouter(prefix="/projects", tags=["Projects"])


# ── Public routes (no auth) ──────────────────────────────────────────


@router.get("", response_model=list[ProjectResponse])
def get_projects() -> list[ProjectResponse]:
    """List all projects (featured first, then newest)."""
    return list_projects()


@router.get("/{slug}", response_model=ProjectResponse)
def get_project(slug: str) -> ProjectResponse:
    """Get a single project by slug."""
    return get_project_by_slug(slug)


# ── Admin routes (require auth) ─────────────────────────────────────


@router.post("", response_model=ProjectResponse, status_code=201)
def create_project_route(
    data: ProjectCreate,
    admin: AdminUser = Depends(require_admin),
) -> ProjectResponse:
    """Create a new project (admin only)."""
    return create_project(data)


@router.put("/{project_id}", response_model=ProjectResponse)
def update_project_route(
    project_id: str,
    data: ProjectUpdate,
    admin: AdminUser = Depends(require_admin),
) -> ProjectResponse:
    """Update an existing project (admin only)."""
    return update_project(project_id, data)


@router.delete("/{project_id}", status_code=204)
def delete_project_route(
    project_id: str,
    admin: AdminUser = Depends(require_admin),
) -> None:
    """Delete a project (admin only)."""
    delete_project(project_id)


@router.post("/upload-image", response_model=ImageUploadResponse)
async def upload_project_image(
    file: UploadFile,
    admin: AdminUser = Depends(require_admin),
) -> ImageUploadResponse:
    """Upload a cover image to Supabase Storage (admin only)."""
    content = await file.read()
    url = upload_image(content, file.filename or "image.png")
    return ImageUploadResponse(url=url)
