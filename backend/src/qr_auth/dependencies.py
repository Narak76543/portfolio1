"""QR Auth domain dependencies."""

from typing import Any
from src.qr_auth import service


def get_qr_request_or_404(request_id: str) -> dict[str, Any]:
    """FastAPI dependency to fetch QR status or raise 404."""
    return service.get_qr_status(request_id)
