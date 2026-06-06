from cryptography.fernet import Fernet
import base64
import hashlib

def get_fernet_key(key):
    # Fernet keys must be 32 bytes and base64 encoded.
    # We hash your Master Key to ensure it's exactly the right length.
    k = hashlib.sha256(str(key).encode()).digest()
    return base64.urlsafe_b64encode(k)

def encrypt(text, key):
    try:
        f_key = get_fernet_key(key)
        f = Fernet(f_key)
        # Fernet returns bytes, so we convert back to string
        return f.encrypt(text.encode()).decode()
    except Exception as e:
        return f"Fernet Encrypt Error: {e}"

def decrypt(text, key):
    try:
        f_key = get_fernet_key(key)
        f = Fernet(f_key)
        # Decrypts and checks integrity automatically
        return f.decrypt(text.encode()).decode()
    except Exception as e:
        return "Fernet Decrypt Error: Key is wrong or message was tampered with!"