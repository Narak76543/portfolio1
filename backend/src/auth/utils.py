"""Auth domain utility functions.

Pure helpers only — no DB session, no request context.
"""


def extract_bearer_token(authorization: str | None) -> str | None:
    """Extract the token from a 'Bearer <token>' header value."""
    if not authorization:
        return None
    parts = authorization.split(" ", 1)
    if len(parts) == 2 and parts[0].lower() == "bearer":
        return parts[1]
    return None
