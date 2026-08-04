"""Stats domain table model."""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class StatItem:
    id: str
    label: str
    value: str
    icon_name: str | None
    display_order: int
    created_at: datetime
