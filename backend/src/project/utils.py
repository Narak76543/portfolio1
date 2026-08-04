"""Project domain utility functions.

Pure helpers only — no DB session, no request context.
"""

import re
import uuid


def generate_slug(title: str) -> str:
    """Generate a URL-friendly slug from a title."""
    slug = title.lower().strip()
    slug = re.sub(r"[^\w\s-]", "", slug)
    slug = re.sub(r"[\s_]+", "-", slug)
    slug = re.sub(r"-+", "-", slug)
    return slug.strip("-")


def generate_unique_filename(original_filename: str) -> str:
    """Generate a unique filename to avoid storage collisions."""
    ext = original_filename.rsplit(".", 1)[-1] if "." in original_filename else "png"
    return f"{uuid.uuid4().hex}.{ext}"
