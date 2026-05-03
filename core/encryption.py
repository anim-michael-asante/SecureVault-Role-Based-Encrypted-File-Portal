import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import base64


MASTER_PASSWORD = b"securevault-master-key-2025"
MASTER_SALT = b"securevault-salt"


def get_master_key():
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=MASTER_SALT,
        iterations=100000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(MASTER_PASSWORD))
    return key


def encrypt_file(file_bytes):
    """Encrypt file bytes, return (encrypted_bytes, file_encryption_key)"""
    file_key = Fernet.generate_key()
    f = Fernet(file_key)
    encrypted = f.encrypt(file_bytes)

    # Encrypt the file key with master key
    master_fernet = Fernet(get_master_key())
    encrypted_file_key = master_fernet.encrypt(file_key)

    return encrypted, encrypted_file_key


def decrypt_file(encrypted_bytes, encrypted_file_key):
    """Decrypt file bytes using the stored encrypted key"""
    master_fernet = Fernet(get_master_key())
    file_key = master_fernet.decrypt(bytes(encrypted_file_key))
    f = Fernet(file_key)
    return f.decrypt(encrypted_bytes)
