"""
Security and Encryption Utilities for StatutoryGuard Encrypted Vault
"""

import base64
import hashlib
import os
from cryptography.fernet import Fernet
from config import VAULT_SECRET_KEY

def _derive_fernet_key(passphrase: str = VAULT_SECRET_KEY) -> bytes:
    """Derive a 32-byte URL-safe base64 key from passphrase."""
    digest = hashlib.sha256(passphrase.encode("utf-8")).digest()
    return base64.urlsafe_b64encode(digest)

def encrypt_bytes(data: bytes, secret_key: str = VAULT_SECRET_KEY) -> bytes:
    """Encrypt raw bytes using AES (Fernet)."""
    key = _derive_fernet_key(secret_key)
    f = Fernet(key)
    return f.encrypt(data)

def decrypt_bytes(token: bytes, secret_key: str = VAULT_SECRET_KEY) -> bytes:
    """Decrypt token bytes using AES (Fernet)."""
    key = _derive_fernet_key(secret_key)
    f = Fernet(key)
    return f.decrypt(token)

def compute_file_hash(data: bytes) -> str:
    """Compute SHA-256 hash for document integrity verification."""
    return hashlib.sha256(data).hexdigest()
