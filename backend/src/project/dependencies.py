"""Project domain FastAPI dependencies."""

from fastapi import Depends

from src.auth.dependencies import get_current_admin
from src.auth.schemas import AdminUser
from src.project.schemas import ProjectResponse
from src.project.service import get_project_by_id


def get_project_or_404(project_id: str) -> ProjectResponse:
    """Dependency that fetches a project or raises ProjectNotFound (404)."""
    return get_project_by_id(project_id)


def require_admin(admin: AdminUser = Depends(get_current_admin)) -> AdminUser:
    """Convenience alias — pass-through to get_current_admin."""
    return admin
