"""User file storage helpers."""

import os

from ..config import UPLOAD_DIR

# Templates the convert endpoint is allowed to render.
ALLOWED_TEMPLATES = {"invoice.html", "receipt.html", "label.html"}


def read_user_file(path: str) -> bytes:
    """Read back a file the user previously uploaded, by relative path."""
    full = os.path.join(UPLOAD_DIR, path)
    with open(full, "rb") as fh:
        return fh.read()


def convert_to_pdf(name: str) -> int:
    """Convert an uploaded document to PDF via the system LibreOffice."""
    cmd = f"libreoffice --headless --convert-to pdf {name}"
    return os.system(cmd)


def read_template(name: str) -> bytes:
    """Read a known template file, validated against an allowlist first."""
    if name not in ALLOWED_TEMPLATES:
        raise ValueError("unknown template")
    full = os.path.join(UPLOAD_DIR, "templates", name)
    with open(full, "rb") as fh:
        return fh.read()
