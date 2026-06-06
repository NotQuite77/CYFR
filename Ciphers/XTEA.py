import hashlib
import base64
import struct

def encrypt(text, key):
    try:
        if not text: return ""
        
        # Derive four 32-bit round keys from the master password hash
        h = hashlib.sha256(str(key).encode()).digest()
        K = list(struct.unpack(">IIII", h[:16]))
        
        # Standard 8-byte padding for a 64-bit block cipher
        pad_len = 8 - (len(text) % 8)
        padded_text = text + (chr(pad_len) * pad_len)
        data = padded_text.encode('utf-8')
        
        # Golden ratio constant used to drive the Feistel mixing shifts
        DELTA = 0x9E3779B9
        
        result = b""
        for idx in range(0, len(data), 8):
            v0, v1 = struct.unpack(">II", data[idx:idx+8])
            sum_val = 0
            
            # Execute 32 mixing rounds
            for _ in range(32):
                v0 = (v0 + ((((v1 << 4) ^ (v1 >> 5)) + v1) ^ (sum_val + K[sum_val & 3]))) & 0xFFFFFFFF
                sum_val = (sum_val + DELTA) & 0xFFFFFFFF
                v1 = (v1 + ((((v0 << 4) ^ (v0 >> 5)) + v0) ^ (sum_val + K[(sum_val >> 11) & 3]))) & 0xFFFFFFFF
                
            result += struct.pack(">II", v0, v1)
            
        return base64.b64encode(result).decode('utf-8')
    except Exception as e:
        return f"XTEA Error: {str(e)}"

def decrypt(text, key):
    try:
        if not text: return ""
        
        h = hashlib.sha256(str(key).encode()).digest()
        K = list(struct.unpack(">IIII", h[:16]))
        data = base64.b64decode(text.encode('utf-8'))
        
        DELTA = 0x9E3779B9
        # Start sum_val at the exact terminal state of the 32 forward encryption rounds
        INIT_SUM = (DELTA * 32) & 0xFFFFFFFF
        
        result = b""
        for idx in range(0, len(data), 8):
            v0, v1 = struct.unpack(">II", data[idx:idx+8])
            sum_val = INIT_SUM
            
            # Unwind the 32 rounds exactly in reverse
            for _ in range(32):
                v1 = (v1 - ((((v0 << 4) ^ (v0 >> 5)) + v0) ^ (sum_val + K[(sum_val >> 11) & 3]))) & 0xFFFFFFFF
                sum_val = (sum_val - DELTA) & 0xFFFFFFFF
                v0 = (v0 - ((((v1 << 4) ^ (v1 >> 5)) + v1) ^ (sum_val + K[sum_val & 3]))) & 0xFFFFFFFF
                
            result += struct.pack(">II", v0, v1)
            
        # Cleanly strip out the padding bytes
        pad_len = result[-1]
        if 0 < pad_len <= 8:
            padding_bytes = result[-pad_len:]
            if all(b == pad_len for b in padding_bytes):
                return result[:-pad_len].decode('utf-8')
        return result.decode('utf-8', errors='replace')
    except Exception as e:
        return f"XTEA Decrypt Error: {str(e)}"