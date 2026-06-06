import base64
import hashlib
from Crypto.Cipher import Salsa20

def encrypt(plaintext, key):
    try:
        # 1. Salsa20 requires a strict 16 or 32-byte key. Hashing guarantees compliance.
        hashed_key = hashlib.sha256(key.encode('utf-8')).digest()
        
        # 2. Check if text is standard string or intermediate latin-1 binary data
        try:
            raw_input_bytes = plaintext.encode('utf-8')
        except UnicodeEncodeError:
            raw_input_bytes = plaintext.encode('latin-1')
            
        # 3. Spin up the Salsa20 engine instance
        cipher = Salsa20.new(key=hashed_key)
        
        # 4. Encrypt (Salsa20 is a stream cipher, so NO padding needed!)
        raw_ciphertext = cipher.encrypt(raw_input_bytes)
        
        # 5. Pack the Nonce and Ciphertext together for loop transport efficiency
        combined_data = cipher.nonce + raw_ciphertext
        
        return base64.b64encode(combined_data).decode('utf-8')
    except Exception as e:
        return f"Salsa20 Error: Encryption failed ({str(e)})"

def decrypt(ciphertext_base64, key):
    try:
        # 1. Re-hash the master key to get the identical 32-byte key layout
        hashed_key = hashlib.sha256(key.encode('utf-8')).digest()
        
        # 2. Decode the Base64 stream safely depending on its chain history
        try:
            combined_data = base64.b64decode(ciphertext_base64.encode('utf-8'))
        except Exception:
            combined_data = ciphertext_base64.encode('latin-1')
            
        # Salsa20 nonces are strictly 8 bytes long
        if len(combined_data) < 8:
            return "Error: Data stream too short to extract Salsa20 nonce vector."
            
        # 3. Extract the 8-byte nonce from the header block
        nonce = combined_data[:8]
        raw_ciphertext = combined_data[8:]
        
        # 4. Re-create the cipher instance using the extracted nonce
        cipher = Salsa20.new(key=hashed_key, nonce=nonce)
        
        # 5. Decrypt directly
        plain_bytes = cipher.decrypt(raw_ciphertext)
        
        # 6. Route output between intermediate chain layers or final readable layout strings
        try:
            return plain_bytes.decode('utf-8')
        except UnicodeDecodeError:
            return plain_bytes.decode('latin-1')
            
    except Exception as e:
        return f"Error: Salsa20 Decryption failed ({str(e)})"