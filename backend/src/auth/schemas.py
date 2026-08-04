"""Auth domain Pydantic schemas."""

from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    """Incoming login payload."""

    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    """Returned after successful login."""

    access_token: str
    token_type: str = "bearer"
    user_id: str
    email: str


class AdminUser(BaseModel):
    """Represents the currently authenticated admin user."""

    id: str
    email: str
