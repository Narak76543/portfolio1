"""Profile domain models.

Represents the Supabase 'profile' table structure.
Since we use the Supabase client (not SQLAlchemy), this serves as
documentation of the table schema.
"""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class ProfileRow:
    """Mirrors the 'profile' table in Supabase/PostgreSQL."""

    id: str
    avatar_url: str | None = None
    tagline: str | None = None
    about_heading: str | None = None
    about_subheading: str | None = None
    about_bio: str | None = None
    logo_type: str | None = "text"
    logo_text: str | None = "SARAT NARAK"
    logo_image_url: str | None = None
    heading_font_url: str | None = None
    heading_font_name: str | None = None
    first_name: str | None = "Sarat"
    last_name: str | None = "Narak"
    hero_pitch: str | None = "I build backend APIs, mobile apps, and web dashboards — and this site is one of my projects too."
    updated_at: datetime | None = None
