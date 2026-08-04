"""Tech stack domain custom exceptions."""

from fastapi import status
from src.exceptions import AppException


class TechStackNotFound(AppException):
    def __init__(self, tech_id: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tech stack item with ID '{tech_id}' was not found.",
        )


class TechStackUploadFailed(AppException):
    def __init__(self, message: str):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Icon upload failed: {message}",
        )


class InvalidIconError(AppException):
    def __init__(self, message: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message,
        )
