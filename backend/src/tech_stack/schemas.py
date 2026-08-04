"""Tech stack domain Pydantic schemas."""

from datetime import datetime
from pydantic import BaseModel, ConfigDict


class TechStackCreate(BaseModel):
    name: str
    icon_url: str | None = None
    display_order: int = 0


class TechStackUpdate(BaseModel):
    name: str | None = None
    icon_url: str | None = None
    display_order: int | None = None


class TechStackResponse(BaseModel):
    id: str
    name: str
    icon_url: str | None = None
    display_order: int = 0
    created_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
