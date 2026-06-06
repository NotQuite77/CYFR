import hashlib
import base64

# Official PRESENT 4-bit S-Box
S_BOX = [0xC, 0x5, 0x6, 0xB, 0x9, 0x0, 0xA, 0xD, 0x3, 0xE, 0xF, 0x8, 0x4, 0x7, 0x1, 0x2]

# Compute Inverse S-Box dynamically for Decryption
INV_S_BOX = [0] * 16
for idx, val in enumerate(S_BOX):
    INV_S_BOX[val] = idx

def transform_s(block_64):
    # Pass all 16 nibbles (4-bit chunks) through the 4-bit S-Box array
    out = 0
    for i in range(16):
        nibble = (block_64 >> (4 * i)) & 0xF
        out |= (S_BOX[nibble] << (4 * i))
    return out

def inv_transform_s(block_64):
    # Undo 4-bit nibble mapping via inverse lookup
    out = 0
    for i in range(16):
        nibble = (block_64 >> (4 * i)) & 0xF
        out |= (INV_S_BOX[nibble] << (4 * i))
    return out

def transform_p(block_64):
    # Official PRESENT 64-bit bit permutation layer mapping
    out = 0
    for i in range(64):
        bit = (block_64 >> i) & 1
        # Permutation rule: P(i) = (16 * i) % 63 for i < 63, and P(63) = 63
        new_pos = (16 * i) % 63 if i < 63 else 63
        out |= (bit << new_pos)
    return out

def inv_transform_p(block_64):
    # Reverse the exact bit permutation layer positional wiring
    out = 0
    for i in range(64):
        bit = (block_64 >> i) & 1
        orig_pos = (4 * i) % 63 if i < 63 else 63
        out |= (bit << orig_pos)
    return out

def get_round_keys(master_key):
    # Generate 31 discrete 64-bit round keys from an 80-bit key schedule slice
    k = hashlib.sha256(str(master_key).encode()).digest()
    key_val = int.from_bytes(k[:10], 'big') # Strip out exactly 80 bits
    
    round_keys = []
    for r in range(1, 32):
        round_keys.append(key_val >> 16) # Top 64 bits are extracted as the round key
        
        # Key register update schedule:
        # 1. Rotate left 61 bits
        key_val = ((key_val << 61) | (key_val >> 19)) & ((1 << 80) - 1)
        # 2. Pass left-most nibble through the S-Box
        left_nibble = (key_val >> 76) & 0xF
        key_val = (key_val & ~((0xF) << 76)) | (S_BOX[left_nibble] << 76)
        # 3. XOR the round counter index into bits 19-15
        key_val ^= (r << 15)
        
    return round_keys

def encrypt(text, key):
    try:
        if not text: return ""
        r_keys = get_round_keys(key)
        
        # Standard 8-byte padding layout tracking
        pad_len = 8 - (len(text) % 8)
        padded_text = text + (chr(pad_len) * pad_len)
        data = padded_text.encode('utf-8')
        
        result = b""
        for idx in range(0, len(data), 8):
            block = int.from_bytes(data[idx:idx+8], 'big')
            
            # Execute 31 rounds of SPN transformations
            for r in range(31):
                block ^= r_keys[r]
                block = transform_s(block)
                block = transform_p(block)
                
            block ^= r_keys[30] # Final terminal key mixing layer
            result += block.to_bytes(8, 'big')
            
        return base64.b64encode(result).decode('utf-8')
    except Exception as e:
        return f"PRESENT Error: {str(e)}"

def decrypt(text, key):
    try:
        if not text: return ""
        r_keys = get_round_keys(key)
        data = base64.b64decode(text.encode('utf-8'))
        
        result = b""
        for idx in range(0, len(data), 8):
            block = int.from_bytes(data[idx:idx+8], 'big')
            
            # Peel off terminal key layer
            block ^= r_keys[30]
            
            # Step backward through the SPN layers exactly in reverse order
            for r in range(30, -1, -1):
                block = inv_transform_p(block)
                block = inv_transform_s(block)
                block ^= r_keys[r]
                
            result += block.to_bytes(8, 'big')
            
        pad_len = result[-1]
        if 0 < pad_len <= 8:
            padding_bytes = result[-pad_len:]
            if all(b == pad_len for b in padding_bytes):
                return result[:-pad_len].decode('utf-8')
        return result.decode('utf-8', errors='replace')
    except Exception as e:
        return f"PRESENT Decrypt Error: {str(e)}"