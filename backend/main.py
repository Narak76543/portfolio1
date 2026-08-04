"""FastAPI Cloud entrypoint re-exporting app instance from src.main."""

from src.main import app

__all__ = ["app"]
