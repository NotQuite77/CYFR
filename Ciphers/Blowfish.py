from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import hashlib
import base64

def get_bf_tools(key):
    # Blowfish needs a specific key size. We hash your key to 32 bytes.
    key_hash = hashlib.sha256(str(key).encode()).digest()
    # Blowfish uses an 8-byte IV
    iv = key_hash[:8]
    return key_hash, iv

def encrypt(text, key):
    try:
        bf_key, iv = get_bf_tools(key)
        cipher = Cipher(algorithms.Blowfish(bf_key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()

        # Blowfish is a block cipher (8-byte blocks), so we must pad the text
        padder = padding.PKCS7(64).padder()
        padded_data = padder.update(text.encode()) + padder.finalize()

        encrypted = encryptor.update(padded_data) + encryptor.finalize()
        return base64.b64encode(encrypted).decode()
    except Exception as e:
        return f"Blowfish Error: {str(e)}"

def decrypt(text, key):
    try:
        bf_key, iv = get_bf_tools(key)
        cipher = Cipher(algorithms.Blowfish(bf_key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()

        raw_data = base64.b64decode(text.encode())
        decrypted_padded = decryptor.update(raw_data) + decryptor.finalize()

        # Remove the padding to get the original text back
        unpadder = padding.PKCS7(64).unpadder()
        result = unpadder.update(decrypted_padded) + unpadder.finalize()
        return result.decode()
    except Exception as e:
        return "Blowfish Decrypt Error: Key mismatch or corrupted data."