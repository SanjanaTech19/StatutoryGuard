"""
Authentication and Password Hashing Utility for StatutoryGuard
Uses PBKDF2 HMAC SHA-256 with secure salt for strict password security.
"""

import hashlib
import secrets

def hash_password(password: str) -> str:
    """Hash password using PBKDF2 with SHA-256 and a random salt."""
    salt = secrets.token_hex(16)
    key = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt.encode('utf-8'),
        100000
    )
    return f"{salt}${key.hex()}"

def verify_password(password: str, hashed_str: str) -> bool:
    """Verify password against stored salt$hash string."""
    try:
        salt, key_hex = hashed_str.split('$')
        key = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt.encode('utf-8'),
            100000
        )
        return secrets.compare_digest(key.hex(), key_hex)
    except Exception:
        return False
