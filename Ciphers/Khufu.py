import hashlib
import base64
import struct

def generate_dynamic_sbox(key_str):
    # Derive a unique 256-entry S-Box of 32-bit words using the master password
    h = hashlib.sha256(str(key_str).encode()).digest()
    
    sbox = []
    for i in range(256):
        # Mutate the seed continuously to generate 256 unique 32-bit integers
        round_seed = hashlib.sha256(h + bytes([i])).digest()
        word = struct.unpack(">I", round_seed[:4])[0]
        sbox.append(word)
    return sbox

def khufu_block(block, sbox, round_keys, encrypt_mode=True):
    # Khufu operates on a 64-bit block split into two 32-bit halves
    L, R = struct.unpack(">I I", block)
    
    # 16 standard rounds of mixing
    if encrypt_mode:
        for r in range(16):
            # Extract the least significant byte of L to use as the S-Box index
            sbox_idx = L & 0xFF
            
            # Non-linear substitution and XOR mixing
            R ^= sbox[sbox_idx]
            
            # Add key material on specific round boundaries (every 4 rounds)
            if r % 4 == 0:
                R = (R + round_keys[r // 4]) & 0xFFFFFFFF
                
            # Swap halves and rotate L to ensure massive data diffusion
            L = ((L >> 8) | (L << 24)) & 0xFFFFFFFF
            L, R = R, L
    else:
        # Decryption exactly mirrors the pipeline backwards
        for r in range(15, -1, -1):
            L, R = R, L
            L = ((L << 8) | (L >> 24)) & 0xFFFFFFFF
            
            if r % 4 == 0:
                R = (R - round_keys[r // 4]) & 0xFFFFFFFF
                
            sbox_idx = L & 0xFF
            R ^= sbox[sbox_idx]
            
    return struct.pack(">I I", L, R)

def encrypt(text, key):
    try:
        if not text: return ""
        sbox = generate_dynamic_sbox(key)
        
        # Derive four 32-bit round keys from the password hash
        h = hashlib.sha256(str(key).encode()).digest()
        round_keys = list(struct.unpack(">IIII", h[16:32]))
        
        # Standard 8-byte block alignment padding
        pad_len = 8 - (len(text) % 8)
        padded_text = text + (chr(pad_len) * pad_len)
        data = padded_text.encode('utf-8')
        
        result = b""
        for i in range(0, len(data), 8):
            result += khufu_block(data[i:i+8], sbox, round_keys, encrypt_mode=True)
            
        return base64.b64encode(result).decode('utf-8')
    except Exception as e:
        return f"Khufu Error: {str(e)}"

def decrypt(text, key):
    try:
        if not text: return ""
        sbox = generate_dynamic_sbox(key)
        
        h = hashlib.sha256(str(key).encode()).digest()
        round_keys = list(struct.unpack(">IIII", h[16:32]))
        data = base64.b64decode(text.encode('utf-8'))
        
        result = b""
        for i in range(0, len(data), 8):
            result += khufu_block(data[i:i+8], sbox, round_keys, encrypt_mode=False)
            
        # Cleanly strip out the trailing padding bytes
        pad_len = result[-1]
        if 0 < pad_len <= 8:
            padding_bytes = result[-pad_len:]
            if all(b == pad_len for b in padding_bytes):
                return result[:-pad_len].decode('utf-8')
        return result.decode('utf-8', errors='replace')
    except Exception as e:
        return f"Khufu Decrypt Error: {str(e)}"