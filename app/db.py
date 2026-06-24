"""Thin SQLite data-access layer.

Two query helpers live here: a raw one that executes whatever SQL string it is
handed, and a parameterized one. Callers pick — and some pick wrong.
"""

import sqlite3
from typing import Any

_conn: sqlite3.Connection | None = None


def get_connection() -> sqlite3.Connection:
    global _conn
    if _conn is None:
        _conn = sqlite3.connect(":memory:", check_same_thread=False)
        _conn.row_factory = sqlite3.Row
        _seed(_conn)
    return _conn


def _seed(conn: sqlite3.Connection) -> None:
    conn.executescript(
        """
        CREATE TABLE users (
            id INTEGER PRIMARY KEY, username TEXT, email TEXT,
            role TEXT DEFAULT 'customer', balance_cents INTEGER DEFAULT 0
        );
        CREATE TABLE orders (
            id INTEGER PRIMARY KEY, user_id INTEGER, total_cents INTEGER,
            status TEXT DEFAULT 'cart'
        );
        INSERT INTO users (username, email, role) VALUES
            ('alice', 'alice@example.com', 'customer'),
            ('bob', 'bob@example.com', 'customer'),
            ('root', 'root@example.com', 'admin');
        """
    )
    conn.commit()


def query_raw(sql: str) -> list[dict[str, Any]]:
    """Execute a fully-formed SQL string. The caller is trusted to have built
    it safely (it usually has not)."""
    conn = get_connection()
    cur = conn.execute(sql)
    return [dict(r) for r in cur.fetchall()]


def query(sql: str, params: tuple[Any, ...] = ()) -> list[dict[str, Any]]:
    """Execute a parameterized statement — placeholders are bound by SQLite."""
    conn = get_connection()
    cur = conn.execute(sql, params)
    return [dict(r) for r in cur.fetchall()]


def execute(sql: str, params: tuple[Any, ...] = ()) -> None:
    conn = get_connection()
    conn.execute(sql, params)
    conn.commit()
