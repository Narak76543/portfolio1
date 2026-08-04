"""QR Auth domain pure helper functions."""

import hashlib
import secrets
from datetime import datetime, timezone


def generate_device_secret() -> str:
    """Generate a 64-character cryptographically secure secret string."""
    return secrets.token_hex(32)


def hash_device_secret(secret: str) -> str:
    """Compute SHA-256 hash of a device secret."""
    return hashlib.sha256(secret.encode("utf-8")).hexdigest()


def parse_iso_utc(dt_str: str) -> datetime:
    """Safely parse ISO datetime string into timezone-aware UTC datetime."""
    dt = datetime.fromisoformat(dt_str.replace("Z", "+00:00"))
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt
