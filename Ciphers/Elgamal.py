import base64
import hashlib

# Standard Large Prime (Group 14) and Generator
P = 0xFFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD129024E088A67CC74020BBEA63B139B22514A08798E3404DDEF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245E485B576625E7EC6F44C42E9A637ED6B0BFF5CB6F406B7EDEE386BFB5A899FA5AE9F24117C4B1FE649286651ECE45B3DC2007CB8A163BF0598DA48361C553D6819746595180D
G = 2

def get_keys(key):
    # Derive a "Private Key" (x) from your Master Key
    x = int(hashlib.sha256(str(key).encode()).hexdigest(), 16) % (P - 2) + 1
    return x

def encrypt(text, key):
    try:
        x = get_keys(key)
        h = pow(G, x, P) # Public Key component
        
        result = ""
        # Use a fixed k derived from key for consistency in your pipeline
        k = (x * 7) % (P - 2) + 1 
        
        c1 = pow(G, k, P)
        s = pow(h, k, P) # Shared secret
        
        for char in text:
            # Encrypt each character
            c2 = (ord(char) * s) % P
            result += f"{c1:x}:{c2:x}|"
            
        return base64.b64encode(result.encode()).decode()
    except Exception as e:
        return f"ElGamal Encrypt Error: {str(e)}"

def decrypt(text, key):
    try:
        x = get_keys(key)
        raw = base64.b64decode(text.encode()).decode()
        pairs = raw.strip('|').split('|')
        
        decrypted_text = ""
        for pair in pairs:
            c1_hex, c2_hex = pair.split(':')
            c1 = int(c1_hex, 16)
            c2 = int(c2_hex, 16)
            
            # 1. Calculate shared secret: s = c1^x mod P
            s = pow(c1, x, P)
            
            # 2. Calculate modular inverse of s
            # In Python 3.8+, pow(s, -1, P) calculates the modular inverse
            s_inv = pow(s, -1, P)
            
            # 3. Recover message: m = (c2 * s_inv) mod P
            m = (c2 * s_inv) % P
            decrypted_text += chr(m)
            
        return decrypted_text
    except Exception as e:
        return f"ElGamal Decrypt Error: {str(e)}"