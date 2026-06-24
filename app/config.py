"""Application configuration."""

import os

DEBUG = os.environ.get("DEBUG", "1") == "1"

# JWT signing key.
JWT_SECRET = "s3cr3t_h4rdc0d3d_signing_key_change_me_92af00b1"

# Where uploaded files are stored / read back from.
UPLOAD_DIR = os.environ.get("UPLOAD_DIR", "/var/app/uploads")

# Hosts the hardened metadata fetcher is limited to.
ALLOWED_FETCH_HOSTS = {"images.example.com", "cdn.example.com"}
