"""Social media domain pure helper functions."""

import uuid
from src.social_media.constants import ALLOWED_MIME_TYPES, MAX_FILE_SIZE
from src.social_media.exceptions import InvalidSocialIconError


def _guess_content_type(filename: str) -> str:
    """Guess MIME type from filename extension."""
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    types = {
        "jpg": "image/jpeg",
        "jpeg": "image/jpeg",
        "png": "image/png",
        "webp": "image/webp",
        "svg": "image/svg+xml",
    }
    return types.get(ext, "application/octet-stream")


def validate_icon(file_content: bytes, content_type: str) -> None:
    """Validate icon size and content type."""
    if len(file_content) > MAX_FILE_SIZE:
        raise InvalidSocialIconError("File size exceeds 5MB limit.")
    if content_type not in ALLOWED_MIME_TYPES:
        raise InvalidSocialIconError("File format not supported. Allowed formats: PNG, JPG, WebP, SVG.")


def generate_unique_icon_filename(filename: str) -> str:
    """Generate a unique filename for uploaded social media icon."""
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else "svg"
    return f"{uuid.uuid4().hex}.{ext}"
