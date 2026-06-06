import hashlib
import base64
import struct

def mul_inv(x):
    if x <= 1:
        return x
    t0, t1 = 0, 1
    r0, r1 = 0x10001, x
    while r1 > 0:
        q = r0 // r1
        r0, r1 = r1, r0 - q * r1
        t0, t1 = t1, t0 - q * t1
    if t0 < 0:
        t0 += 0x10001
    return t0 & 0xFFFF

def mul(x, y):
    x = 0x10001 - x if x == 0 else x & 0xFFFF
    y = 0x10001 - y if y == 0 else y & 0xFFFF
    res = (x * y) % 0x10001
    return 0 if res == 0x10001 else res & 0xFFFF

def add(x, y):
    return (x + y) & 0xFFFF

def add_inv(x):
    return (0x10000 - x) & 0xFFFF

def generate_subkeys(key_bytes):
    key_val = int.from_bytes(key_bytes, 'big')
    subkeys = []
    for _ in range(7):
        for i in range(8):
            subkeys.append((key_val >> (112 - 16 * i)) & 0xFFFF)
        key_val = ((key_val << 25) | (key_val >> 103)) & ((1 << 128) - 1)
    return subkeys[:52]

def generate_decryption_keys(enc_keys):
    dec_keys = [0] * 52
    
    # Round 1 decryption keys mapped from Round 9 encryption keys
    dec_keys[0] = mul_inv(enc_keys[48])
    dec_keys[1] = add_inv(enc_keys[49])
    dec_keys[2] = add_inv(enc_keys[50])
    dec_keys[3] = mul_inv(enc_keys[51])
    dec_keys[4] = enc_keys[46]
    dec_keys[5] = enc_keys[47]
    
    # Intermediate rounds 2 through 8
    for r in range(1, 8):
        p = r * 6
        i = 48 - r * 6
        dec_keys[p]     = mul_inv(enc_keys[i])
        dec_keys[p + 1] = add_inv(enc_keys[i + 2])
        dec_keys[p + 2] = add_inv(enc_keys[i + 1])
        dec_keys[p + 3] = mul_inv(enc_keys[i + 3])
        dec_keys[p + 4] = enc_keys[i - 2]
        dec_keys[p + 5] = enc_keys[i - 1]
        
    # Final half-round transformation keys
    dec_keys[48] = mul_inv(enc_keys[0])
    dec_keys[49] = add_inv(enc_keys[1])
    dec_keys[50] = add_inv(enc_keys[2])
    dec_keys[51] = mul_inv(enc_keys[3])
    
    return dec_keys

def idea_crypt_block(block, keys):
    x1, x2, x3, x4 = struct.unpack(">HHHH", block)
    for r in range(8):
        p = r * 6
        x1 = mul(x1, keys[p])
        x2 = add(x2, keys[p + 1])
        x3 = add(x3, keys[p + 2])
        x4 = mul(x4, keys[p + 3])
        
        t1 = x1 ^ x3
        t2 = x2 ^ x4
        t1 = mul(t1, keys[p + 4])
        t2 = add(t2, t1)
        t2 = mul(t2, keys[p + 5])
        t1 = add(t1, t2)
        
        x1 ^= t2
        x4 ^= t1
        x2, x3 = x3 ^ t2, x2 ^ t1
        
    # Output transformation round
    x1 = mul(x1, keys[48])
    x2, x3 = add(x3, keys[49]), add(x2, keys[50]) # Swapped block alignment natively here
    x4 = mul(x4, keys[51])
    return struct.pack(">HHHH", x1, x2, x3, x4)

def get_key_bytes(key):
    return hashlib.sha256(str(key).encode()).digest()[:16]

def encrypt(text, key):
    try:
        key_bytes = get_key_bytes(key)
        enc_keys = generate_subkeys(key_bytes)
        
        pad_len = 8 - (len(text) % 8)
        padded_text = text + (chr(pad_len) * pad_len)
        data = padded_text.encode('utf-8')
        
        result = b""
        for i in range(0, len(data), 8):
            result += idea_crypt_block(data[i:i+8], enc_keys)
        return base64.b64encode(result).decode('utf-8')
    except Exception as e:
        return f"IDEA Error: {str(e)}"

def decrypt(text, key):
    try:
        key_bytes = get_key_bytes(key)
        enc_keys = generate_subkeys(key_bytes)
        dec_keys = generate_decryption_keys(enc_keys)
        
        data = base64.b64decode(text.encode('utf-8'))
        result = b""
        for i in range(0, len(data), 8):
            result += idea_crypt_block(data[i:i+8], dec_keys)
            
        pad_len = result[-1]
        if 0 < pad_len <= 8:
            return result[:-pad_len].decode('utf-8')
        return result.decode('utf-8')
    except Exception as e:
        return f"IDEA Decrypt Error: {str(e)}"