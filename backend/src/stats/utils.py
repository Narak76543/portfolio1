"""Stats domain pure helper functions."""


def sanitize_stat_value(value: str) -> str:
    """Sanitize stat card value string."""
    return value.strip()
