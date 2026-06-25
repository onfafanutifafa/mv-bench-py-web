"""Application configuration."""

import os

DEBUG = os.environ.get("DEBUG", "1") == "1"

# JWT signing key.
JWT_SECRET = "xJ8kP3vNq7Lw2RtZ9cF4bM6hY1aD5sG0eU8iQwBzC"

# Where uploaded files are stored / read back from.
UPLOAD_DIR = os.environ.get("UPLOAD_DIR", "/var/app/uploads")

# Hosts the hardened metadata fetcher is limited to.
ALLOWED_FETCH_HOSTS = {"images.example.com", "cdn.example.com"}
