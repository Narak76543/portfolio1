"""QR Auth domain exceptions."""

from src.exceptions import AppException


class QRRequestNotFound(AppException):
    def __init__(self, message: str = "QR login request not found."):
        super().__init__(message=message, status_code=404)


class QRRequestExpired(AppException):
    def __init__(self, message: str = "QR code has expired. Please refresh for a new QR code."):
        super().__init__(message=message, status_code=400)


class InvalidDeviceSecret(AppException):
    def __init__(self, message: str = "Device secret is invalid or this device is not trusted."):
        super().__init__(message=message, status_code=401)


class DeviceNotFound(AppException):
    def __init__(self, message: str = "Trusted device not found."):
        super().__init__(message=message, status_code=404)
