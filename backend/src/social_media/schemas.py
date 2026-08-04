"""Social media domain Pydantic schemas."""

from datetime import datetime
from pydantic import BaseModel, ConfigDict


class SocialMediaCreate(BaseModel):
    name: str
    value: str
    url: str
    icon_url: str | None = None
    display_order: int = 0


class SocialMediaUpdate(BaseModel):
    name: str | None = None
    value: str | None = None
    url: str | None = None
    icon_url: str | None = None
    display_order: int | None = None


class SocialMediaResponse(BaseModel):
    id: str
    name: str
    value: str
    url: str
    icon_url: str | None = None
    display_order: int = 0
    created_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
