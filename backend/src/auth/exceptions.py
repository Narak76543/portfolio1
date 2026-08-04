"""Auth domain exceptions."""

from src.auth.constants import (
    ERROR_AUTH_FAILED,
    ERROR_INVALID_CREDENTIALS,
    ERROR_TOKEN_EXPIRED,
    ERROR_TOKEN_MISSING,
)
from src.exceptions import AppException


class InvalidCredentials(AppException):
    """Raised when email/password are wrong."""

    def __init__(self) -> None:
        super().__init__(
            status_code=401,
            detail="Invalid email or password.",
            error_code=ERROR_INVALID_CREDENTIALS,
        )


class TokenMissing(AppException):
    """Raised when no Bearer token is provided."""

    def __init__(self) -> None:
        super().__init__(
            status_code=401,
            detail="Authentication token is missing.",
            error_code=ERROR_TOKEN_MISSING,
        )


class TokenExpired(AppException):
    """Raised when the JWT has expired."""

    def __init__(self) -> None:
        super().__init__(
            status_code=401,
            detail="Authentication token has expired.",
            error_code=ERROR_TOKEN_EXPIRED,
        )


class AuthFailed(AppException):
    """Generic auth failure (e.g. Supabase returned an error)."""

    def __init__(self, detail: str = "Authentication failed.") -> None:
        super().__init__(
            status_code=401,
            detail=detail,
            error_code=ERROR_AUTH_FAILED,
        )
