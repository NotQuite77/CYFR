import hashlib
import base64
import struct

def rotate_left(val, shift):
    # Perform a clean 32-bit circular rotation to the left
    return ((val << shift) | (val >> (32 - shift))) & 0xFFFFFFFF

def multi2_round_pi1(v0, v1, k):
    # Multi2 elementary round function Pi1
    v0 = (v0 + k[0]) & 0xFFFFFFFF
    v1 = (v1 ^ v0) & 0xFFFFFFFF
    return v0, v1

def multi2_round_pi2(v0, v1, k):
    # Multi2 elementary round function Pi2
    v0 = (v0 ^ (v1 + k[1])) & 0xFFFFFFFF
    return v0, v1

def multi2_round_pi3(v0, v1, k):
    # Multi2 elementary round function Pi3
    shift = (k[2] & 7) + 1
    v1 = (v1 + rotate_left(v0, shift)) & 0xFFFFFFFF
    v0 = (v0 ^ v1) & 0xFFFFFFFF
    return v0, v1

def multi2_round_pi4(v0, v1, k):
    # Multi2 elementary round function Pi4
    v1 = (v1 ^ (v0 + k[3])) & 0xFFFFFFFF
    return v0, v1

def multi2_block(block, round_keys, encrypt_mode=True):
    # Multi2 runs over two 32-bit words (64-bit block size)
    v0, v1 = struct.unpack(">II", block)
    
    # 4 core key parameters per round iteration execution block
    k = round_keys[:4]
    
    if encrypt_mode:
        # Forward execution pipeline
        v0, v1 = multi2_round_pi1(v0, v1, k)
        v0, v1 = multi2_round_pi2(v0, v1, k)
        v0, v1 = multi2_round_pi3(v0, v1, k)
        v0, v1 = multi2_round_pi4(v0, v1, k)
    else:
        # Reversing Multi2 is exceptionally clean because each step is a pure involution
        # Undo Pi4
        v1 = (v1 ^ (v0 + k[3])) & 0xFFFFFFFF
        # Undo Pi3
        v0 = (v0 ^ v1) & 0xFFFFFFFF
        shift = (k[2] & 7) + 1
        v1 = (v1 - rotate_left(v0, shift)) & 0xFFFFFFFF
        # Undo Pi2
        v0 = (v0 ^ (v1 + k[1])) & 0xFFFFFFFF
        # Undo Pi1
        v1 = (v1 ^ v0) & 0xFFFFFFFF
        v0 = (v0 - k[0]) & 0xFFFFFFFF
        
    return struct.pack(">II", v0 & 0xFFFFFFFF, v1 & 0xFFFFFFFF)

def encrypt(text, key):
    try:
        if not text: return ""
        # Derive uniform 32-bit internal keys from master password hash
        h = hashlib.sha256(str(key).encode()).digest()
        round_keys = list(struct.unpack(">IIIIIIII", h))
        
        # 8-byte block alignment padding loop tracking
        pad_len = 8 - (len(text) % 8)
        padded_text = text + (chr(pad_len) * pad_len)
        data = padded_text.encode('utf-8')
        
        result = b""
        for i in range(0, len(data), 8):
            result += multi2_block(data[i:i+8], round_keys, encrypt_mode=True)
            
        return base64.b64encode(result).decode('utf-8')
    except Exception as e:
        return f"Multi2 Error: {str(e)}"

def decrypt(text, key):
    try:
        if not text: return ""
        h = hashlib.sha256(str(key).encode()).digest()
        round_keys = list(struct.unpack(">IIIIIIII", h))
        data = base64.b64decode(text.encode('utf-8'))
        
        result = b""
        for i in range(0, len(data), 8):
            result += multi2_block(data[i:i+8], round_keys, encrypt_mode=False)
            
        # Extract the trailing padding bits clean out
        pad_len = result[-1]
        if 0 < pad_len <= 8:
            padding_bytes = result[-pad_len:]
            if all(b == pad_len for b in padding_bytes):
                return result[:-pad_len].decode('utf-8')
        return result.decode('utf-8', errors='replace')
    except Exception as e:
        return f"Multi2 Decrypt Error: {str(e)}"