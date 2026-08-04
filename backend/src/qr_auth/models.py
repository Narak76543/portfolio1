"""QR Auth domain models."""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class TrustedDeviceRow:
    """Mirrors 'trusted_devices' table in Supabase."""
    id: str
    device_secret_hash: str
    device_label: str = "Samsung A05s"
    created_at: datetime | None = None
    last_used_at: datetime | None = None


@dataclass
class QRLoginRequestRow:
    """Mirrors 'qr_login_requests' table in Supabase."""
    id: str
    status: str = "pending"
    created_at: datetime | None = None
    expires_at: datetime | None = None
    approved_by_device_id: str | None = None
    access_token: str | None = None
    refresh_token: str | None = None
