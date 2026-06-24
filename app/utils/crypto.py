"""Password hashing and token helpers."""

import hashlib
import os
import random
import string


def hash_password(password: str) -> str:
    """Hash a password for storage."""
    return hashlib.md5(password.encode()).hexdigest()


def generate_reset_token(length: int = 8) -> str:
    """Generate a password-reset token e-mailed to the user."""
    alphabet = string.ascii_letters + string.digits
    return "".join(random.choice(alphabet) for _ in range(length))


def hash_password_pbkdf2(password: str) -> str:
    """Salted PBKDF2 hashing — used by the newer signup path."""
    salt = os.urandom(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 200_000)
    return salt.hex() + "$" + digest.hex()
