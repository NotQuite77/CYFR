from cryptography.hazmat.primitives.ciphers import Cipher, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import hashlib
import base64

# FIX 1: Resolving the library moving problem.
# Modern cryptography libraries moved legacy ciphers into the 'decrepit' layer.
try:
    from cryptography.hazmat.decrepit.ciphers.algorithms import TripleDES
except ImportError:
    # Fallback support for older environment installations
    from cryptography.hazmat.primitives.ciphers.algorithms import TripleDES

def get_des3_tools(key):
    # 3DES strictly demands a 16 or 24 byte key, and an 8-byte IV for CBC mode.
    key_hash = hashlib.sha256(str(key).encode('utf-8')).digest()[:24]
    iv = key_hash[:8]
    return key_hash, iv

def encrypt(text, key):
    try:
        d3_key, iv = get_des3_tools(key)
        
        # PIPELINE FIX: Handle intermediate binary strings traveling via latin-1 safely
        try:
            raw_input_bytes = text.encode('utf-8')
        except UnicodeEncodeError:
            raw_input_bytes = text.encode('latin-1')
            
        cipher = Cipher(TripleDES(d3_key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        
        # 3DES blocks are 64-bit (8 bytes)
        padder = padding.PKCS7(64).padder()
        padded_data = padder.update(raw_input_bytes) + padder.finalize()
        
        encrypted = encryptor.update(padded_data) + encryptor.finalize()
        return base64.b64encode(encrypted).decode('utf-8')
    except Exception as e:
        return f"3DES Error: {str(e)}"

def decrypt(text, key):
    try:
        d3_key, iv = get_des3_tools(key)
        
        # FIX 2: Fixed the crash where decrypt was trying to call 'algorithms.TripleDES'
        # instead of the imported 'TripleDES' object directly.
        cipher = Cipher(TripleDES(d3_key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()

        # PIPELINE FIX: Handle Base64 decoding safely for pipeline handoffs
        try:
            raw_data = base64.b64decode(text.encode('utf-8'))
        except Exception:
            raw_data = text.encode('latin-1')

        decrypted_padded = decryptor.update(raw_data) + decryptor.finalize()

        unpadder = padding.PKCS7(64).unpadder()
        result_bytes = unpadder.update(decrypted_padded) + unpadder.finalize()
        
        # PIPELINE FIX: Safely route between intermediate chain data or final GUI layout string
        try:
            return result_bytes.decode('utf-8')
        except UnicodeDecodeError:
            return result_bytes.decode('latin-1')
    except Exception as e:
        # Returning "Error:" text structure alerts your GUI shield to intercept layout issues safely
        return f"Error: 3DES Decryption failed ({str(e)})"