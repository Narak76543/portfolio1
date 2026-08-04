"""QR Auth domain router."""

from fastapi import APIRouter, Depends, Request, status
from src.auth.dependencies import get_current_admin
from src.qr_auth import service
from src.qr_auth.schemas import (
    ApproveQRRequest,
    RegisterDeviceRequest,
    RegisterDeviceResponse,
    StartQRResponse,
    TrustedDeviceResponse,
)

router = APIRouter(prefix="/qr-auth", tags=["qr-auth"])


@router.post(
    "/register-device",
    response_model=RegisterDeviceResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(get_current_admin)],
)
def register_device(data: RegisterDeviceRequest) -> RegisterDeviceResponse:
    """Register a device as trusted for QR approval (Admin only)."""
    return service.register_trusted_device(data)


@router.get(
    "/devices",
    response_model=list[TrustedDeviceResponse],
    dependencies=[Depends(get_current_admin)],
)
def list_devices() -> list[TrustedDeviceResponse]:
    """List all trusted devices for QR login (Admin only)."""
    return service.list_trusted_devices()


@router.delete(
    "/devices/{device_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(get_current_admin)],
)
def revoke_device(device_id: str) -> None:
    """Revoke a trusted device by ID (Admin only)."""
    service.revoke_trusted_device(device_id)


@router.post("/start", response_model=StartQRResponse)
def start_qr_request(request: Request) -> StartQRResponse:
    """Start a new short-lived QR login request (Public)."""
    origin = request.headers.get("origin") or "http://localhost:3002"
    return service.start_qr_request(base_frontend_url=origin)


@router.get("/status/{request_id}")
def check_qr_status(request_id: str) -> dict:
    """Check the status of a QR login request (Public)."""
    return service.get_qr_status(request_id)


@router.post("/approve/{request_id}")
def approve_qr(request_id: str, data: ApproveQRRequest) -> dict:
    """Approve a QR login request using stored phone device_secret (Public)."""
    return service.approve_qr_request(request_id, data.device_secret)
