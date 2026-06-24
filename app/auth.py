"""Minimal session/auth helpers.

A real deployment would verify a signed JWT; here we decode a base64 'uid:role'
token to keep the sample importable without extra dependencies. The point is the
*shape*: a current-user dependency exists, and some routes forget to use it.
"""

import base64

from fastapi import Header, HTTPException

from . import db
from .models import User


def _load_user(user_id: int) -> User | None:
    rows = db.query("SELECT * FROM users WHERE id = ?", (user_id,))
    if not rows:
        return None
    r = rows[0]
    return User(id=r["id"], username=r["username"], email=r["email"], role=r["role"])


def current_user(authorization: str = Header(default="")) -> User:
    """FastAPI dependency: resolve the caller from an 'Bearer <b64 uid:role>'
    header. Raises 401 when absent or malformed."""
    token = authorization.removeprefix("Bearer ").strip()
    if not token:
        raise HTTPException(status_code=401, detail="missing token")
    try:
        uid_str, _role = base64.b64decode(token).decode().split(":", 1)
        user = _load_user(int(uid_str))
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=401, detail="bad token") from exc
    if user is None:
        raise HTTPException(status_code=401, detail="unknown user")
    return user


def require_admin(user: User) -> None:
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="admin only")
