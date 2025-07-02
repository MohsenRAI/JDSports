# security_config.py
"""
Security configuration and validation functions
"""
import os
import mimetypes
from pathlib import Path

# Security settings
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp"}
ALLOWED_MIME_TYPES = {"image/png", "image/jpeg", "image/gif", "image/bmp", "image/webp"}


def validate_image_file(file):
    """
    Validate uploaded image file for security

    Args:
        file: Flask file object

    Returns:
        tuple: (is_valid, error_message)
    """
    if not file or not file.filename:
        return False, "No file provided"

    # Check file extension
    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        return False, f"Invalid file type. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"

    # Check MIME type
    mime_type, _ = mimetypes.guess_type(file.filename)
    if mime_type not in ALLOWED_MIME_TYPES:
        return False, "Invalid file format"

    # Check file size
    file.seek(0, 2)  # Seek to end
    file_size = file.tell()
    file.seek(0)  # Reset to beginning

    if file_size > MAX_FILE_SIZE:
        return False, f"File too large. Maximum size: {MAX_FILE_SIZE // (1024*1024)}MB"

    if file_size == 0:
        return False, "Empty file"

    return True, None


def sanitize_path(path):
    """
    Sanitize file path to prevent directory traversal

    Args:
        path: Input path string

    Returns:
        str: Sanitized path
    """
    if not path:
        return ""

    # Remove dangerous characters and patterns
    sanitized = path.replace("..", "").replace("//", "/").replace("\\", "/")
    sanitized = sanitized.strip("/")

    # Remove any null bytes
    sanitized = sanitized.replace("\x00", "")

    return sanitized


def validate_path_within_base(file_path, base_path):
    """
    Ensure file path is within the allowed base directory

    Args:
        file_path: Target file path
        base_path: Allowed base directory

    Returns:
        bool: True if path is safe
    """
    try:
        # Resolve absolute paths
        abs_file_path = os.path.abspath(file_path)
        abs_base_path = os.path.abspath(base_path)

        # Check if file path starts with base path
        return abs_file_path.startswith(abs_base_path)
    except (OSError, ValueError):
        return False


# Rate limiting settings (for future implementation)
RATE_LIMIT_REQUESTS = 10  # requests per minute
RATE_LIMIT_WINDOW = 60  # seconds

# Security headers
SECURITY_HEADERS = {
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "X-XSS-Protection": "1; mode=block",
    "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
    "Content-Security-Policy": "default-src 'self'; img-src 'self' data: https:; script-src 'self'",
}
