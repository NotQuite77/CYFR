import hashlib
import base64
import struct

# Official GOST Magma S-Box
S_BOX = [
    [12, 4, 6, 2, 10, 5, 11, 9, 14, 8, 13, 7, 0, 3, 15, 1],
    [6, 8, 2, 3, 9, 10, 5, 12, 1, 14, 4, 7, 11, 13, 0, 15],
    [11, 3, 5, 8, 2, 15, 10, 13, 14, 1, 7, 4, 12, 9, 6, 0],
    [12, 8, 2, 1, 13, 4, 15, 6, 7, 0, 10, 5, 3, 14, 9, 11],
    [7, 15, 5, 10, 8, 1, 6, 13, 0, 9, 3, 14, 11, 4, 2, 12],
    [5, 13, 15, 6, 9, 2, 12, 10, 11, 7, 8, 1, 4, 3, 14, 0],
    [8, 14, 2, 5, 6, 9, 1, 12, 15, 4, 11, 0, 13, 10, 3, 7],
    [1, 7, 14, 13, 0, 5, 8, 3, 4, 15, 10, 6, 9, 12, 11, 2]
]

def f_func(part, key_part):
    temp = (part + key_part) % (2**32)
    output = 0
    for i in range(8):
        nibble = (temp >> (4 * i)) & 0xf
        output |= (S_BOX[i][nibble] << (4 * i))
    return ((output << 11) | (output >> (32 - 11))) & 0xffffffff

def gost_block(block, keys, mode='encrypt'):
    left, right = struct.unpack(">II", block)
    
    # The GOST key schedule is specific:
    # Encrypt: K0...K7, K0...K7, K0...K7, K7...K0 (32 rounds)
    # Decrypt: K0...K7, K7...K0, K7...K0, K7...K0 (Basically reversed)
    
    # Let's create the specific 32-round sequence
    if mode == 'encrypt':
        round_keys = list(keys) * 3 + list(keys)[::-1]
    else:
        round_keys = list(keys)[:8][::-1] + list(keys)[:8] * 3
        # Simplest way to decrypt a Feistel: Reverse the EXACT sequence used to encrypt
        round_keys = (list(keys) * 3 + list(keys)[::-1])[::-1]

    for k in round_keys:
        left, right = right, left ^ f_func(right, k)
    
    # Final swap and pack
    return struct.pack(">II", right, left)

def get_keys(key):
    h = hashlib.sha256(str(key).encode()).digest()
    return struct.unpack(">IIIIIIII", h)

def encrypt(text, key):
    try:
        subkeys = get_keys(key)
        # Padding
        pad_len = 8 - (len(text) % 8)
        text += chr(pad_len) * pad_len
        data = text.encode()
        
        result = b""
        for i in range(0, len(data), 8):
            result += gost_block(data[i:i+8], subkeys)
        return base64.b64encode(result).decode()
    except Exception as e:
        return f"GOST Error: {str(e)}"

def decrypt(text, key):
    try:
        subkeys = get_keys(key)
        data = base64.b64decode(text.encode())
        
        result = b""
        for i in range(0, len(data), 8):
            # Pass mode='decrypt' to use the reversed key sequence
            result += gost_block(data[i:i+8], subkeys, mode='decrypt')
        
        # Remove padding safely
        pad_len = result[-1]
        if 0 < pad_len <= 8:
            return result[:-pad_len].decode('utf-8')
        return result.decode('utf-8')
    except Exception as e:
        # If it still fails, it's likely the math produced non-UTF8 junk
        return f"GOST Decrypt Error: Key mismatch (Math failed to produce valid text)"
        
        # --- SAFER PADDING REMOVAL ---
        if not result:
            return "[GOST Error: No Data]"
            
        pad_len = result[-1]
        
        # Validate pad_len to prevent "blank" output errors
        if 0 < pad_len <= 8:
            return result[:-pad_len].decode('utf-8')
        else:
            return result.decode('utf-8') # Return as-is if padding looks wrong
            
    except Exception as e:
        return f"GOST Decrypt Error: {str(e)}"