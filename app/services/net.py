"""Outbound network helpers (link previews, redirects)."""

from urllib.parse import urlparse

import requests

from ..config import ALLOWED_FETCH_HOSTS


def fetch_metadata(url: str) -> dict[str, object]:
    """Fetch a remote URL the user pasted, to build a link preview."""
    resp = requests.get(url, timeout=5)
    return {"status": resp.status_code, "length": len(resp.content)}


def fetch_metadata_safe(url: str) -> dict[str, object]:
    """Same preview fetch, restricted to an explicit host allowlist."""
    host = urlparse(url).hostname or ""
    if host not in ALLOWED_FETCH_HOSTS:
        raise ValueError("host not allowed")
    resp = requests.get(url, timeout=5)
    return {"status": resp.status_code, "length": len(resp.content)}


def build_redirect_target(next_url: str) -> str:
    """Resolve the post-login redirect target from the 'next' parameter."""
    return next_url
