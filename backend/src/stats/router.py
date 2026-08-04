"""Stats domain router."""

from fastapi import APIRouter, Depends, status
from src.auth.dependencies import get_current_admin
from src.stats import service
from src.stats.schemas import StatCreate, StatResponse, StatUpdate

router = APIRouter(prefix="/stats", tags=["stats"])


@router.get("", response_model=list[StatResponse])
def list_stats() -> list[StatResponse]:
    """Get all stat cards ordered by display_order (Public)."""
    return service.list_stats()


@router.post(
    "",
    response_model=StatResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(get_current_admin)],
)
def create_stat(data: StatCreate) -> StatResponse:
    """Create a new stat card (Admin only)."""
    return service.create_stat(data)


@router.put(
    "/{stat_id}",
    response_model=StatResponse,
    dependencies=[Depends(get_current_admin)],
)
def update_stat(stat_id: str, data: StatUpdate) -> StatResponse:
    """Update a stat card (Admin only)."""
    return service.update_stat(stat_id, data)


@router.delete(
    "/{stat_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(get_current_admin)],
)
def delete_stat(stat_id: str) -> None:
    """Delete a stat card (Admin only)."""
    service.delete_stat(stat_id)
