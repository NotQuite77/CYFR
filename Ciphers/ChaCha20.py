from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
import os

def encrypt(text, key):
    # 1. Key Derivation
    # ChaCha20-Poly1305 requires a 32-byte key.
    # We'll hash your Master Key to ensure it's the right length.
    import hashlib
    k = hashlib.sha256(str(key).encode()).digest()
    
    chacha = ChaCha20Poly1305(k)
    
    # 2. Generate a Nonce (Number used once)
    # This is like the IV in AES.
    nonce = os.urandom(12)
    
    # 3. Encrypt
    # The 'None' is for 'Associated Data' which we aren't using here.
    ciphertext = chacha.encrypt(nonce, text.encode(), None)
    
    # Return Nonce + Ciphertext in hex
    return (nonce + ciphertext).hex()

def decrypt(text, key):
    try:
        # 1. Convert hex to bytes
        data = bytes.fromhex(text)
        nonce = data[:12]
        ciphertext = data[12:]
        
        # 2. Re-derive the 32-byte key
        import hashlib
        k = hashlib.sha256(str(key).encode()).digest()
        
        chacha = ChaCha20Poly1305(k)
        
        # 3. Decrypt
        decrypted_data = chacha.decrypt(nonce, ciphertext, None)
        return decrypted_data.decode('utf-8')
    except Exception as e:
        return f"ChaCha20 Decrypt Error: {e}"