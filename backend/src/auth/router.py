"""Auth domain router — HTTP layer only, no business logic."""

from fastapi import APIRouter, Depends

from src.auth.dependencies import get_current_admin
from src.auth.schemas import AdminUser, LoginRequest, LoginResponse
from src.auth.service import login_with_email_password

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=LoginResponse)
def login(payload: LoginRequest) -> LoginResponse:
    """Authenticate admin user via email/password."""
    response = login_with_email_password(payload.email, payload.password)

    session = response.session
    user = response.user

    # session and user are guaranteed non-None by the service layer
    assert session is not None
    assert user is not None

    return LoginResponse(
        access_token=session.access_token,
        user_id=user.id,
        email=user.email or "",
    )


@router.get("/me", response_model=AdminUser)
def get_me(admin: AdminUser = Depends(get_current_admin)) -> AdminUser:
    """Return the currently authenticated admin user."""
    return admin
