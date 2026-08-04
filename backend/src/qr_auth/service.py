"""QR Auth domain service — ALL database queries and logic live here."""

from datetime import datetime, timedelta, timezone
from typing import Any

from src.database import get_supabase_client
from src.qr_auth.constants import QR_EXPIRATION_SECONDS, QR_REQUESTS_TABLE, TRUSTED_DEVICES_TABLE
from src.qr_auth.exceptions import (
    DeviceNotFound,
    InvalidDeviceSecret,
    QRRequestExpired,
    QRRequestNotFound,
)
from src.qr_auth.schemas import (
    RegisterDeviceRequest,
    RegisterDeviceResponse,
    StartQRResponse,
    TrustedDeviceResponse,
)
from src.qr_auth.utils import generate_device_secret, hash_device_secret, parse_iso_utc


def register_trusted_device(data: RegisterDeviceRequest) -> RegisterDeviceResponse:
    """Register a new trusted device, return device_secret to store in phone's localStorage."""
    client = get_supabase_client()
    raw_secret = generate_device_secret()
    secret_hash = hash_device_secret(raw_secret)

    payload = {
        "device_secret_hash": secret_hash,
        "device_label": data.device_label.strip() or "Samsung A05s",
    }

    result = client.table(TRUSTED_DEVICES_TABLE).insert(payload).execute()
    row = result.data[0]

    return RegisterDeviceResponse(
        device_id=str(row["id"]),
        device_secret=raw_secret,
        device_label=row["device_label"],
        created_at=row.get("created_at"),
    )


def list_trusted_devices() -> list[TrustedDeviceResponse]:
    """Get list of all trusted devices."""
    client = get_supabase_client()
    result = (
        client.table(TRUSTED_DEVICES_TABLE)
        .select("*")
        .order("created_at", desc=True)
        .execute()
    )
    return [
        TrustedDeviceResponse(
            id=str(row["id"]),
            device_label=row["device_label"],
            created_at=row.get("created_at"),
            last_used_at=row.get("last_used_at"),
        )
        for row in result.data
    ]


def revoke_trusted_device(device_id: str) -> None:
    """Revoke (delete) a trusted device by ID."""
    client = get_supabase_client()
    result = client.table(TRUSTED_DEVICES_TABLE).select("*").eq("id", device_id).execute()
    if not result.data:
        raise DeviceNotFound()
    client.table(TRUSTED_DEVICES_TABLE).delete().eq("id", device_id).execute()


def start_qr_request(base_frontend_url: str = "http://localhost:3002") -> StartQRResponse:
    """Start a new short-lived QR login request (90 seconds)."""
    client = get_supabase_client()
    now_utc = datetime.now(timezone.utc)
    expires_at = now_utc + timedelta(seconds=QR_EXPIRATION_SECONDS)

    payload = {
        "status": "pending",
        "expires_at": expires_at.isoformat(),
    }

    result = client.table(QR_REQUESTS_TABLE).insert(payload).execute()
    row = result.data[0]
    request_id = str(row["id"])

    approval_url = f"{base_frontend_url}/qr-approve/{request_id}"

    return StartQRResponse(
        id=request_id,
        approval_url=approval_url,
        expires_at=expires_at,
    )


def get_qr_status(request_id: str) -> dict[str, Any]:
    """Get the current status of a QR login request."""
    client = get_supabase_client()
    result = client.table(QR_REQUESTS_TABLE).select("*").eq("id", request_id).execute()
    if not result.data:
        raise QRRequestNotFound()

    row = result.data[0]
    status = row["status"]

    # Check expiration if pending
    if status == "pending":
        expires_at_str = row.get("expires_at")
        if expires_at_str:
            expires_at = parse_iso_utc(expires_at_str)
            if datetime.now(timezone.utc) > expires_at:
                client.table(QR_REQUESTS_TABLE).update({"status": "expired"}).eq("id", request_id).execute()
                status = "expired"

    return {
        "id": str(row["id"]),
        "status": status,
        "access_token": row.get("access_token") if status == "approved" else None,
        "refresh_token": row.get("refresh_token") if status == "approved" else None,
    }


def approve_qr_request(request_id: str, device_secret: str) -> dict[str, str]:
    """Approve a QR login request using a phone's trusted device secret."""
    client = get_supabase_client()

    # 1. Verify device secret against trusted_devices
    secret_hash = hash_device_secret(device_secret)
    device_result = (
        client.table(TRUSTED_DEVICES_TABLE)
        .select("*")
        .eq("device_secret_hash", secret_hash)
        .execute()
    )
    if not device_result.data:
        raise InvalidDeviceSecret()

    device_row = device_result.data[0]
    device_id = str(device_row["id"])

    # 2. Verify QR request is valid and not expired
    req_result = client.table(QR_REQUESTS_TABLE).select("*").eq("id", request_id).execute()
    if not req_result.data:
        raise QRRequestNotFound()

    req_row = req_result.data[0]
    if req_row["status"] != "pending":
        raise QRRequestExpired("QR code is no longer pending.")

    expires_at_str = req_row.get("expires_at")
    if expires_at_str:
        expires_at = parse_iso_utc(expires_at_str)
        if datetime.now(timezone.utc) > expires_at:
            client.table(QR_REQUESTS_TABLE).update({"status": "expired"}).eq("id", request_id).execute()
            raise QRRequestExpired()

    # 3. Generate admin auth session
    users = client.auth.admin.list_users()
    if not users:
        raise InvalidDeviceSecret("No admin user found to issue session.")

    admin_email = users[0].email
    link = client.auth.admin.generate_link({"type": "magiclink", "email": admin_email})
    otp = link.properties.email_otp
    verify_res = client.auth.verify_otp({"email": admin_email, "token": otp, "type": "magiclink"})

    if not verify_res.session:
        raise InvalidDeviceSecret("Failed to generate admin session.")

    access_token = verify_res.session.access_token
    refresh_token = verify_res.session.refresh_token

    # 4. Update qr_login_requests row
    now_iso = datetime.now(timezone.utc).isoformat()
    client.table(QR_REQUESTS_TABLE).update({
        "status": "approved",
        "approved_by_device_id": device_id,
        "access_token": access_token,
        "refresh_token": refresh_token,
    }).eq("id", request_id).execute()

    # 5. Update trusted_devices last_used_at
    client.table(TRUSTED_DEVICES_TABLE).update({
        "last_used_at": now_iso,
    }).eq("id", device_id).execute()

    return {"message": "Login approved successfully!"}
