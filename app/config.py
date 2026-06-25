"""Application configuration."""

import os

DEBUG = os.environ.get("DEBUG", "1") == "1"

# JWT signing key.
JWT_SECRET = "9f2c4a7e1b8d3f6092e5c1a4b7d0f3e6a9c2b5d8e1f4a7c0b3d6e9f2a5c8b1d4e"

# Where uploaded files are stored / read back from.
UPLOAD_DIR = os.environ.get("UPLOAD_DIR", "/var/app/uploads")

# Hosts the hardened metadata fetcher is limited to.
ALLOWED_FETCH_HOSTS = {"images.example.com", "cdn.example.com"}
