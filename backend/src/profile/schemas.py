"""Profile domain schemas (Pydantic)."""

from datetime import datetime
from pydantic import BaseModel, ConfigDict


class ProfileResponse(BaseModel):
    """Schema for returning a profile."""
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

    model_config = ConfigDict(from_attributes=True)


class ProfileUpdate(BaseModel):
    """Schema for updating profile fields."""
    tagline: str | None = None
    avatar_url: str | None = None
    about_heading: str | None = None
    about_subheading: str | None = None
    about_bio: str | None = None
    logo_type: str | None = None
    logo_text: str | None = None
    logo_image_url: str | None = None
    heading_font_url: str | None = None
    heading_font_name: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    hero_pitch: str | None = None
