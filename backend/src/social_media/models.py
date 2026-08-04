"""Social media domain table model."""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class SocialMediaItem:
    id: str
    name: str
    value: str
    url: str
    icon_url: str | None
    display_order: int
    created_at: datetime
