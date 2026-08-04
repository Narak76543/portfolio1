"""Stats domain Pydantic schemas."""

from datetime import datetime
from pydantic import BaseModel, ConfigDict


class StatCreate(BaseModel):
    label: str
    value: str
    icon_name: str | None = None
    display_order: int = 0


class StatUpdate(BaseModel):
    label: str | None = None
    value: str | None = None
    icon_name: str | None = None
    display_order: int | None = None


class StatResponse(BaseModel):
    id: str
    label: str
    value: str
    icon_name: str | None = None
    display_order: int = 0
    created_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
