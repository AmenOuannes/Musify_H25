import os

from cryptography.fernet import Fernet
import base64
import hashlib

def generate_key(password: str) -> bytes:
    # Derive a Fernet key from your chosen password
    return base64.urlsafe_b64encode(hashlib.sha256(password.encode()).digest())

def encrypt_password(password: str, key: bytes) -> bytes:
    f = Fernet(key)
    return f.encrypt(password.encode())

def decrypt_password(token: bytes, key: bytes) -> str:
    f = Fernet(key)
    return f.decrypt(token).decode()

key_password = os.getenv("KEY_PASSWORD")
KEY = generate_key(key_password)