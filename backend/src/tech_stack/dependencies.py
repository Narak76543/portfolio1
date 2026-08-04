"""Tech stack domain FastAPI dependencies."""

from src.tech_stack import service
from src.tech_stack.schemas import TechStackResponse


def get_tech_stack_or_404(tech_id: str) -> TechStackResponse:
    """Dependency to retrieve a tech stack item by ID or raise 404."""
    return service.get_tech_stack_by_id(tech_id)
