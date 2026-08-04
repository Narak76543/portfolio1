"""Social media domain FastAPI dependencies."""

from src.social_media import service
from src.social_media.schemas import SocialMediaResponse


def get_social_media_or_404(social_id: str) -> SocialMediaResponse:
    """Dependency to retrieve a social media item by ID or raise 404."""
    return service.get_social_media_by_id(social_id)
