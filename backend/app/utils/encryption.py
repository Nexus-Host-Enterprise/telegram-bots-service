from cryptography.fernet import Fernet
from app.core.config import settings

def get_fernet():
    return Fernet(settings.FERNET_KEY.encode())

def encrypt_token(token: str) -> bytes:
    f = get_fernet()
    return f.encrypt(token.encode())

def decrypt_token(token_encrypted: bytes) -> str:
    f = get_fernet()
    return f.decrypt(token_encrypted).decode()
