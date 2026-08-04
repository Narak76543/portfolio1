"""Base application exception.

All domain-specific exceptions inherit from AppException so the global
exception handler in main.py can catch them uniformly.
"""


class AppException(Exception):
    """Base exception with HTTP status code and machine-readable error code."""

    def __init__(
        self,
        status_code: int = 500,
        detail: str = "An unexpected error occurred.",
        error_code: str = "INTERNAL_ERROR",
    ) -> None:
        self.status_code = status_code
        self.detail = detail
        self.error_code = error_code
        super().__init__(detail)
