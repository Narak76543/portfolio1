"""Profile domain exceptions."""

from fastapi import status
from src.exceptions import AppException


class ProfileNotFound(AppException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found",
        )


class ImageUploadFailed(AppException):
    def __init__(self, message: str):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Image upload failed: {message}",
        )


class InvalidImageError(AppException):
    def __init__(self, message: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message,
        )


class FontUploadFailed(AppException):
    def __init__(self, message: str):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Font upload failed: {message}",
        )


class InvalidFontError(AppException):
    def __init__(self, message: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message,
        )
