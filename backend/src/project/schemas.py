"""Project domain Pydantic schemas.

Never expose models.py directly — all API I/O goes through these schemas.
"""

from datetime import datetime

from pydantic import BaseModel


class ProjectCreate(BaseModel):
    """Schema for creating a new project."""

    title: str
    slug: str
    short_description: str | None = None
    full_description: str | None = None
    tech_stack: list[str] = []
    role: str | None = None
    github_url: str | None = None
    live_url: str | None = None
    cover_image_url: str | None = None
    featured: bool = False
    display_order: int = 0


class ProjectUpdate(BaseModel):
    """Schema for updating an existing project. All fields optional."""

    title: str | None = None
    slug: str | None = None
    short_description: str | None = None
    full_description: str | None = None
    tech_stack: list[str] | None = None
    role: str | None = None
    github_url: str | None = None
    live_url: str | None = None
    cover_image_url: str | None = None
    featured: bool | None = None
    display_order: int | None = None


class ProjectResponse(BaseModel):
    """Schema for returning a project to the client."""

    id: str
    title: str
    slug: str
    short_description: str | None = None
    full_description: str | None = None
    tech_stack: list[str] = []
    role: str | None = None
    github_url: str | None = None
    live_url: str | None = None
    cover_image_url: str | None = None
    featured: bool = False
    display_order: int = 0
    created_at: datetime


class ImageUploadResponse(BaseModel):
    """Returned after a successful image upload."""

    url: str
