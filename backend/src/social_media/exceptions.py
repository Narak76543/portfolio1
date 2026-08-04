"""Social media domain custom exceptions."""

from fastapi import status
from src.exceptions import AppException


class SocialMediaNotFound(AppException):
    def __init__(self, social_id: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Social media item with ID '{social_id}' was not found.",
        )


class SocialMediaUploadFailed(AppException):
    def __init__(self, message: str):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Icon upload failed: {message}",
        )


class InvalidSocialIconError(AppException):
    def __init__(self, message: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message,
        )
