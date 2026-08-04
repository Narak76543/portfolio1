"""Stats domain FastAPI dependencies."""

from src.stats import service
from src.stats.schemas import StatResponse


def get_stat_or_404(stat_id: str) -> StatResponse:
    """Dependency to retrieve a stat item by ID or raise 404."""
    return service.get_stat_by_id(stat_id)
