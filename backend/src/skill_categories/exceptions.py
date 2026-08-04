"""Skill categories domain exceptions."""

from src.exceptions import AppException


class SkillCategoryNotFound(AppException):
    def __init__(self, message: str = "Skill category not found."):
        super().__init__(message=message, status_code=404)
