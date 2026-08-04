"""Profile domain constants."""

TABLE_NAME = "profile"
STORAGE_BUCKET = "project-images"
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
MAX_FONT_FILE_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_MIME_TYPES = ["image/jpeg", "image/png", "image/webp"]
ALLOWED_FONT_EXTENSIONS = [".woff2", ".woff", ".ttf"]
ALLOWED_FONT_MIME_TYPES = [
    "font/woff2",
    "font/woff",
    "font/ttf",
    "application/font-woff",
    "application/font-woff2",
    "font/sfnt",
    "application/x-font-ttf",
    "application/octet-stream",
]
