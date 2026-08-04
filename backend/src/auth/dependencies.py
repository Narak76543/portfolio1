"""Auth domain FastAPI dependencies."""

from fastapi import Request

from src.auth.exceptions import TokenMissing
from src.auth.schemas import AdminUser
from src.auth.service import get_user_from_token
from src.auth.utils import extract_bearer_token


def get_current_admin(request: Request) -> AdminUser:
    """Dependency that extracts and validates the Bearer token.

    Raises TokenMissing if no token is present, or AuthFailed/TokenExpired
    if the token is invalid.
    """
    raw_header = request.headers.get("authorization")
    token = extract_bearer_token(raw_header)

    if token is None:
        raise TokenMissing()

    user_response = get_user_from_token(token)
    user = user_response.user

    return AdminUser(
        id=user.id,
        email=user.email or "",
    )
