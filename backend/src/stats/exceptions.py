"""Stats domain custom exceptions."""

from fastapi import status
from src.exceptions import AppException


class StatNotFound(AppException):
    def __init__(self, stat_id: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Stat item with ID '{stat_id}' was not found.",
        )
