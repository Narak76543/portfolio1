"""Tech stack domain table model."""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class TechStackItem:
    id: str
    name: str
    icon_url: str | None
    display_order: int
    created_at: datetime
