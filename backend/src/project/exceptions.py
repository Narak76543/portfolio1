"""Project domain exceptions."""

from src.exceptions import AppException
from src.project.constants import (
    ERROR_IMAGE_UPLOAD_FAILED,
    ERROR_PROJECT_NOT_FOUND,
    ERROR_PROJECT_SLUG_CONFLICT,
)


class ProjectNotFound(AppException):
    """Raised when a project lookup fails."""

    def __init__(self, identifier: str = "") -> None:
        detail = f"Project not found: {identifier}" if identifier else "Project not found."
        super().__init__(
            status_code=404,
            detail=detail,
            error_code=ERROR_PROJECT_NOT_FOUND,
        )


class ProjectSlugConflict(AppException):
    """Raised when a slug is already taken."""

    def __init__(self, slug: str) -> None:
        super().__init__(
            status_code=409,
            detail=f"A project with slug '{slug}' already exists.",
            error_code=ERROR_PROJECT_SLUG_CONFLICT,
        )


class ImageUploadFailed(AppException):
    """Raised when an image cannot be uploaded to Supabase Storage."""

    def __init__(self, detail: str = "Image upload failed.") -> None:
        super().__init__(
            status_code=500,
            detail=detail,
            error_code=ERROR_IMAGE_UPLOAD_FAILED,
        )
