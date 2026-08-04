"""Social media domain router."""

from fastapi import APIRouter, Depends, File, UploadFile, status
from src.auth.dependencies import get_current_admin
from src.social_media import service
from src.social_media.schemas import SocialMediaCreate, SocialMediaResponse, SocialMediaUpdate

router = APIRouter(prefix="/social-media", tags=["social-media"])


@router.get("", response_model=list[SocialMediaResponse])
def list_social_medias() -> list[SocialMediaResponse]:
    """Get all social media items ordered by display_order (Public)."""
    return service.list_social_medias()


@router.post(
    "",
    response_model=SocialMediaResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(get_current_admin)],
)
def create_social_media(data: SocialMediaCreate) -> SocialMediaResponse:
    """Create a new social media link item (Admin only)."""
    return service.create_social_media(data)


@router.put(
    "/{social_id}",
    response_model=SocialMediaResponse,
    dependencies=[Depends(get_current_admin)],
)
def update_social_media(social_id: str, data: SocialMediaUpdate) -> SocialMediaResponse:
    """Update a social media item (Admin only)."""
    return service.update_social_media(social_id, data)


@router.delete(
    "/{social_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(get_current_admin)],
)
def delete_social_media(social_id: str) -> None:
    """Delete a social media item (Admin only)."""
    service.delete_social_media(social_id)


@router.post(
    "/upload-icon",
    response_model=dict[str, str],
    dependencies=[Depends(get_current_admin)],
)
def upload_icon(file: UploadFile = File(...)) -> dict[str, str]:
    """Upload an icon for a social media item (Admin only)."""
    file_content = file.file.read()
    filename = file.filename or "icon.svg"
    url = service.upload_icon(file_content, filename)
    return {"url": url}
