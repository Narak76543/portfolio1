"""Auth domain service — business logic and Supabase Auth calls."""

from supabase_auth.types import AuthResponse, UserResponse

from src.auth.exceptions import AuthFailed, InvalidCredentials
from src.database import get_supabase_client


def login_with_email_password(email: str, password: str) -> AuthResponse:
    """Authenticate via Supabase Auth and return the session."""
    client = get_supabase_client()
    try:
        response: AuthResponse = client.auth.sign_in_with_password(
            {"email": email, "password": password}
        )
    except Exception as exc:
        raise InvalidCredentials() from exc

    if response.session is None:
        raise InvalidCredentials()

    return response


def get_user_from_token(access_token: str) -> UserResponse:
    """Validate an access token and return the user."""
    client = get_supabase_client()
    try:
        user_response: UserResponse = client.auth.get_user(access_token)
    except Exception as exc:
        raise AuthFailed(detail="Failed to verify token.") from exc

    if user_response.user is None:
        raise AuthFailed(detail="Token is invalid or expired.")

    return user_response
