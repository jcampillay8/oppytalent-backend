import os
from cryptography.fernet import Fernet
from app.config import settings

def get_fernet():
    key = settings.ENCRYPTION_KEY
    if not key:
        raise Exception("ENCRYPTION_KEY not set in environment variables")
    return Fernet(key.encode('utf-8'))

def encrypt_value(value: str) -> str:
    if not value:
        return value
    f = get_fernet()
    return f.encrypt(value.encode('utf-8')).decode('utf-8')

def decrypt_value(encrypted_value: str) -> str:
    if not encrypted_value:
        return encrypted_value
    f = get_fernet()
    return f.decrypt(encrypted_value.encode('utf-8')).decode('utf-8')
