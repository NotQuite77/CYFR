import hashlib
import base64

def generate_keystream(key_str, length):
    # Expand the master key using SHA-256 to create a long, deterministic stream of bytes
    keystream = bytearray()
    counter = 0
    while len(keystream) < length:
        # Mutate the seed with a counter so each block of 32 bytes is unique
        seed = f"{key_str}_{counter}".encode('utf-8')
        keystream.extend(hashlib.sha256(seed).digest())
        counter += 1
    return keystream[:length]

def rotate_left(byte_val, shift):
    # Rotate an 8-bit byte to the left
    shift %= 8
    return ((byte_val << shift) | (byte_val >> (8 - shift))) & 0xFF

def rotate_right(byte_val, shift):
    # Rotate an 8-bit byte to the right (to undo left rotation)
    shift %= 8
    return ((byte_val >> shift) | (byte_val << (8 - shift))) & 0xFF

def encrypt(text, key):
    try:
        if not text: return ""
        data = text.encode('utf-8')
        k_stream = generate_keystream(str(key), len(data))
        
        result = bytearray()
        for idx, byte in enumerate(data):
            k_byte = k_stream[idx]
            
            # Step 1: Add structural offset
            step1 = (byte + k_byte) & 0xFF
            
            # Step 2: Rotate bits left (shift amount determined by key byte)
            shift_amount = (k_byte % 7) + 1  # Shift between 1 and 7 bits
            step2 = rotate_left(step1, shift_amount)
            
            # Step 3: Final bitwise XOR mask
            step3 = step2 ^ k_byte
            
            result.append(step3)
            
        return base64.b64encode(result).decode('utf-8')
    except Exception as e:
        return f"ORX Error: {str(e)}"

def decrypt(text, key):
    try:
        if not text: return ""
        data = base64.b64decode(text.encode('utf-8'))
        k_stream = generate_keystream(str(key), len(data))
        
        result = bytearray()
        for idx, byte in enumerate(data):
            k_byte = k_stream[idx]
            shift_amount = (k_byte % 7) + 1
            
            # Step 1: Undo the final XOR mask
            step1 = byte ^ k_byte
            
            # Step 2: Rotate bits back to the right
            step2 = rotate_right(step1, shift_amount)
            
            # Step 3: Subtract the structural offset out
            step3 = (step2 - k_byte) & 0xFF
            
            result.append(step3)
            
        return result.decode('utf-8')
    except Exception as e:
        return f"ORX Decrypt Error: {str(e)}"