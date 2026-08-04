from fastapi import APIRouter, Depends, File, UploadFile, status
from src.auth.dependencies import get_current_admin
from src.profile import service
from src.profile.schemas import ProfileResponse, ProfileUpdate

router = APIRouter(prefix="/profile", tags=["profile"])

@router.get("", response_model=ProfileResponse)
def get_profile() -> ProfileResponse:
    """Get the current profile."""
    return service.get_profile()


@router.put(
    "",
    response_model=ProfileResponse,
    dependencies=[Depends(get_current_admin)],
)
def update_profile(data: ProfileUpdate) -> ProfileResponse:
    """Update profile fields such as tagline (Admin only)."""
    return service.update_profile(data)
    

@router.post(
    "/upload-avatar",
    response_model=ProfileResponse,
    dependencies=[Depends(get_current_admin)],
)
def upload_avatar(file: UploadFile = File(...)) -> ProfileResponse:
    """Upload a new avatar for the profile (Admin only)."""
    file_content = file.file.read()
    filename = file.filename or "avatar.png"
    return service.update_avatar(file_content, filename)


@router.post(
    "/upload-logo",
    response_model=ProfileResponse,
    dependencies=[Depends(get_current_admin)],
)
def upload_logo(file: UploadFile = File(...)) -> ProfileResponse:
    """Upload a new logo image for the brand header (Admin only)."""
    file_content = file.file.read()
    filename = file.filename or "logo.png"
    return service.upload_logo_image(file_content, filename)


@router.post(
    "/upload-font",
    response_model=ProfileResponse,
    dependencies=[Depends(get_current_admin)],
)
def upload_font(
    font_name: str | None = None,
    file: UploadFile = File(...),
) -> ProfileResponse:
    """Upload a custom font file (.woff2, .woff, or .ttf) for heading text (Admin only)."""
    file_content = file.file.read()
    filename = file.filename or "font.ttf"
    return service.upload_heading_font(file_content, filename, font_name)
