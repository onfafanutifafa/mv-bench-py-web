"""Session (de)serialization helpers."""

import base64
import json
import pickle
from typing import Any


def load_session(blob: str) -> Any:
    """Rebuild a session object from a client-supplied cookie blob."""
    raw = base64.b64decode(blob)
    return pickle.loads(raw)


def dump_session(obj: Any) -> str:
    return base64.b64encode(pickle.dumps(obj)).decode()


def load_preferences(blob: str) -> dict[str, Any]:
    """Read a JSON preferences blob."""
    data = json.loads(base64.b64decode(blob))
    return data if isinstance(data, dict) else {}
