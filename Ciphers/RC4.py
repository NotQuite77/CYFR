import hashlib
import base64

def rc4_crypt(data_bytes, key_str):
    # Derive a deterministic key stream from the master password
    key_bytes = hashlib.sha256(key_str.encode('utf-8')).digest()
    key_len = len(key_bytes)
    
    # --- Phase 1: KSA (Key Scheduling Algorithm) ---
    # Initialize the 256-byte state vector array
    S = list(range(256))
    
    j = 0
    for i in range(256):
        j = (j + S[i] + key_bytes[i % key_len]) % 256
        S[i], S[j] = S[j], S[i] # Swap elements
        
    # --- Phase 2: PRGA (Pseudo-Random Generation Algorithm) ---
    # Walk through the state array to generate key bytes and XOR the data
    i = 0
    j = 0
    result = bytearray()
    
    for byte in data_bytes:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i] # Continually mutate the state table
        
        # Select the keystream byte
        k_byte = S[(S[i] + S[j]) % 256]
        
        # XOR the data stream with the keystream
        result.append(byte ^ k_byte)
        
    return bytes(result)

def encrypt(text, key):
    try:
        if not text: return ""
        data = text.encode('utf-8')
        encrypted_bytes = rc4_crypt(data, str(key))
        return base64.b64encode(encrypted_bytes).decode('utf-8')
    except Exception as e:
        return f"RC4 Error: {str(e)}"

def decrypt(text, key):
    try:
        if not text: return ""
        data = base64.b64decode(text.encode('utf-8'))
        # Stream ciphers use identical math forward and backward
        decrypted_bytes = rc4_crypt(data, str(key))
        return decrypted_bytes.decode('utf-8')
    except Exception as e:
        return f"RC4 Decrypt Error: {str(e)}"