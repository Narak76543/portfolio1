"""Project domain models.

Represents the Supabase 'projects' table structure.
Since we use the Supabase client (not SQLAlchemy), this serves as
documentation of the table schema.
"""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class ProjectRow:
    """Mirrors the 'projects' table in Supabase/PostgreSQL."""

    id: str
    title: str
    slug: str
    short_description: str | None = None
    full_description: str | None = None
    tech_stack: list[str] = field(default_factory=list)
    role: str | None = None
    github_url: str | None = None
    live_url: str | None = None
    cover_image_url: str | None = None
    featured: bool = False
    display_order: int = 0
    created_at: datetime | None = None
