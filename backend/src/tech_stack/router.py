"""Tech stack domain router."""

from fastapi import APIRouter, Depends, File, UploadFile, status
from src.auth.dependencies import get_current_admin
from src.tech_stack import service
from src.tech_stack.schemas import TechStackCreate, TechStackResponse, TechStackUpdate

router = APIRouter(prefix="/tech-stack", tags=["tech-stack"])


@router.get("", response_model=list[TechStackResponse])
def list_tech_stacks() -> list[TechStackResponse]:
    """Get all tech stack items ordered by display_order (Public)."""
    return service.list_tech_stacks()


@router.post(
    "",
    response_model=TechStackResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(get_current_admin)],
)
def create_tech_stack(data: TechStackCreate) -> TechStackResponse:
    """Create a new tech stack item (Admin only)."""
    return service.create_tech_stack(data)


@router.put(
    "/{tech_id}",
    response_model=TechStackResponse,
    dependencies=[Depends(get_current_admin)],
)
def update_tech_stack(tech_id: str, data: TechStackUpdate) -> TechStackResponse:
    """Update a tech stack item (Admin only)."""
    return service.update_tech_stack(tech_id, data)


@router.delete(
    "/{tech_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(get_current_admin)],
)
def delete_tech_stack(tech_id: str) -> None:
    """Delete a tech stack item (Admin only)."""
    service.delete_tech_stack(tech_id)


@router.post(
    "/upload-icon",
    response_model=dict[str, str],
    dependencies=[Depends(get_current_admin)],
)
def upload_icon(file: UploadFile = File(...)) -> dict[str, str]:
    """Upload an icon for a tech stack item (Admin only)."""
    file_content = file.file.read()
    filename = file.filename or "icon.svg"
    url = service.upload_icon(file_content, filename)
    return {"url": url}
