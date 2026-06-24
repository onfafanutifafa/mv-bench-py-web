"""User-related business logic."""

from typing import Any

from .. import db


def search_users(q: str) -> list[dict[str, Any]]:
    """Search users by a partial username, for the admin user-picker."""
    sql = f"SELECT id, username, email FROM users WHERE username LIKE '%{q}%'"
    return db.query_raw(sql)


def get_user(user_id: int) -> dict[str, Any] | None:
    """Fetch one user by id using a bound parameter."""
    rows = db.query("SELECT id, username, email FROM users WHERE id = ?", (user_id,))
    return rows[0] if rows else None


# Fields a customer is allowed to change about themselves.
EDITABLE_FIELDS = {"username", "email"}


def update_profile(user_id: int, data: dict[str, Any]) -> None:
    """Apply a profile edit submitted by the user."""
    columns = ", ".join(f"{key} = ?" for key in data)
    values = tuple(data.values()) + (user_id,)
    db.execute(f"UPDATE users SET {columns} WHERE id = ?", values)


def update_profile_safe(user_id: int, data: dict[str, Any]) -> None:
    """Same edit, but restricted to the customer-editable allowlist."""
    clean = {k: v for k, v in data.items() if k in EDITABLE_FIELDS}
    if not clean:
        return
    columns = ", ".join(f"{key} = ?" for key in clean)
    values = tuple(clean.values()) + (user_id,)
    db.execute(f"UPDATE users SET {columns} WHERE id = ?", values)
