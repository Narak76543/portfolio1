from src.profile.constants import (
    ALLOWED_FONT_EXTENSIONS,
    ALLOWED_FONT_MIME_TYPES,
    ALLOWED_MIME_TYPES,
    MAX_FILE_SIZE,
    MAX_FONT_FILE_SIZE,
)
from src.profile.exceptions import InvalidFontError, InvalidImageError


def validate_image(file_content: bytes, content_type: str) -> None:
    if content_type not in ALLOWED_MIME_TYPES:
        raise InvalidImageError("Only JPEG, PNG, and WebP images are allowed.")
    if len(file_content) > MAX_FILE_SIZE:
        raise InvalidImageError("Image size must be under 5MB.")


def validate_font(file_content: bytes, filename: str) -> None:
    ext = "." + filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    if ext not in ALLOWED_FONT_EXTENSIONS:
        raise InvalidFontError("Only .woff2, .woff, and .ttf font files are allowed.")
    if len(file_content) > MAX_FONT_FILE_SIZE:
        raise InvalidFontError("Font file size must be under 10MB.")


def _guess_content_type(filename: str) -> str:
    """Guess the MIME type from a filename extension."""
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    content_types = {
        "jpg": "image/jpeg",
        "jpeg": "image/jpeg",
        "png": "image/png",
        "webp": "image/webp",
    }
    return content_types.get(ext, "application/octet-stream")


def _guess_font_content_type(filename: str) -> str:
    """Guess the font MIME type from a filename extension."""
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    content_types = {
        "woff2": "font/woff2",
        "woff": "font/woff",
        "ttf": "font/ttf",
    }
    return content_types.get(ext, "font/ttf")
