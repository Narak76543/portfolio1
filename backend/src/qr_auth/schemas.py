"""QR Auth domain Pydantic schemas."""

from datetime import datetime
from pydantic import BaseModel, ConfigDict


class RegisterDeviceRequest(BaseModel):
    device_label: str = "Samsung A05s"


class RegisterDeviceResponse(BaseModel):
    device_id: str
    device_secret: str
    device_label: str
    created_at: datetime | None = None


class StartQRResponse(BaseModel):
    id: str
    approval_url: str
    expires_at: datetime


class QRStatusResponse(BaseModel):
    id: str
    status: str  # pending | approved | expired
    access_token: str | None = None
    refresh_token: str | None = None


class ApproveQRRequest(BaseModel):
    device_secret: str


class TrustedDeviceResponse(BaseModel):
    id: str
    device_label: str
    created_at: datetime | None = None
    last_used_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
