import hashlib
import base64
import struct

def generate_sbox(key_str):
    # Derive a reliable seed from the master password using SHA-256
    seed = hashlib.sha256(str(key_str).encode()).digest()
    
    # Initialize a basic 256-entry S-Box array with 32-bit integer registers
    S = list(range(256))
    # Use the key seed to shuffle the baseline table deterministically
    j = 0
    for i in range(256):
        j = (j + S[i] + seed[i % len(seed)]) % 256
        S[i], S[j] = S[j], S[i]
        
    # Scale up the 8-bit shuffled table into full 32-bit pseudo-random words
    sbox = [0] * 256
    for i in range(256):
        w_seed = hashlib.sha256(bytes([S[i]]) + seed).digest()
        sbox[i] = int.from_bytes(w_seed[:4], 'big') & 0xFFFFFFFF
    return sbox

def M_func(x, y, sbox):
    # Core non-linear WAKE register mixing step function
    sum_val = (x + y) & 0xFFFFFFFF
    return ((sum_val >> 8) ^ sbox[sum_val & 255]) & 0xFFFFFFFF

def encrypt(text, key):
    try:
        if not text: return ""
        sbox = generate_sbox(key)
        
        # Standardize data to 4-byte (32-bit word) alignment tracking boundaries
        pad_len = 4 - (len(text) % 4)
        padded_text = text + (chr(pad_len) * pad_len)
        data = padded_text.encode('utf-8')
        
        # Derive initial state markers for the 4 core tracking registers
        h = hashlib.md5(str(key).encode()).digest()
        A, B, C, D = struct.unpack(">IIII", h)
        
        result = b""
        for idx in range(0, len(data), 4):
            W = int.from_bytes(data[idx:idx+4], 'big')
            
            # XOR with active keystream layer register
            Z = W ^ D
            result += Z.to_bytes(4, 'big')
            
            # Autokey Step: Mutate state registers using the outgoing ciphertext block
            A = M_func(A, Z, sbox)
            B = M_func(B, A, sbox)
            C = M_func(C, B, sbox)
            D = M_func(D, C, sbox)
            
        return base64.b64encode(result).decode('utf-8')
    except Exception as e:
        return f"WAKE Error: {str(e)}"

def decrypt(text, key):
    try:
        if not text: return ""
        sbox = generate_sbox(key)
        data = base64.b64decode(text.encode('utf-8'))
        
        h = hashlib.md5(str(key).encode()).digest()
        A, B, C, D = struct.unpack(">IIII", h)
        
        result = b""
        for idx in range(0, len(data), 4):
            Z = int.from_bytes(data[idx:idx+4], 'big')
            
            # Reverse XOR step to uncover original text data layer word
            W = Z ^ D
            result += W.to_bytes(4, 'big')
            
            # Autokey feedback loops use identical cipher states to track mutations
            A = M_func(A, Z, sbox)
            B = M_func(B, A, sbox)
            C = M_func(C, B, sbox)
            D = M_func(D, C, sbox)
            
        # Extract the trailing padding bits clean out
        pad_len = result[-1]
        if 0 < pad_len <= 4:
            padding_bytes = result[-pad_len:]
            if all(b == pad_len for b in padding_bytes):
                return result[:-pad_len].decode('utf-8')
        return result.decode('utf-8', errors='replace')
    except Exception as e:
        return f"WAKE Decrypt Error: {str(e)}"