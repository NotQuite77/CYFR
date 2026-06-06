import hashlib
import random
import string

def get_seed(key):
    """Turns the Master Key into a deterministic numeric seed for the shuffler."""
    return int(hashlib.sha256(str(key).encode('utf-8')).hexdigest(), 16)

def encrypt(text, key):
    try:
        if not text:
            return ""
            
        seed = get_seed(key)
        
        # 1. Convert text directly to bits via clean byte sequence representation
        raw_bytes = text.encode('utf-8')
        bits = []
        for byte in raw_bytes:
            bits.extend([int(b) for b in format(byte, '08b')])
        
        # 2. Create index map and shuffle
        indices = list(range(len(bits)))
        random.Random(seed).shuffle(indices)
        
        # 3. Permute bits using the shuffled map
        jumbled_bits = [0] * len(bits)
        for i, bit in enumerate(bits):
            jumbled_bits[indices[i]] = bit
            
        # 4. FIXED: Convert bits directly to a raw bytearray, bypassing bad character conversions
        output_bytes = bytearray()
        for i in range(0, len(jumbled_bits), 8):
            byte_chunk = jumbled_bits[i:i+8]
            byte_val = int("".join(map(str, byte_chunk)), 2)
            output_bytes.append(byte_val)
            
        # Output clean, reliable hex
        return output_bytes.hex()
        
    except Exception as e:
        return f"Jumble Error: {str(e)}"

def decrypt(hex_text, key):
    try:
        # 1. Clean boundary strings
        cleaned_hex = str(hex_text).strip()
        
        # 2. Safety Guards
        hex_digits = set(string.hexdigits)
        if not all(char in hex_digits for char in cleaned_hex):
            return "Jumble Decrypt Skip: Input is normal text, not valid hex data."
            
        if not cleaned_hex:
            return "Jumble Decrypt Skip: Input text is empty."

        seed = get_seed(key)
        
        # 3. FIXED: Decode hex directly to raw bytes instead of text strings
        raw_bytes = bytes.fromhex(cleaned_hex)
        jumbled_bits = []
        for byte in raw_bytes:
            jumbled_bits.extend([int(b) for b in format(byte, '08b')])
        
        # 4. Recreate shuffle index map
        indices = list(range(len(jumbled_bits)))
        random.Random(seed).shuffle(indices)
        
        # 5. Reverse the bit mapping sequence
        original_bits = [0] * len(jumbled_bits)
        for i, idx in enumerate(indices):
            original_bits[i] = jumbled_bits[idx]
            
        # 6. Assemble bits back into raw byte arrays
        decrypted_bytes = bytearray()
        for i in range(0, len(original_bits), 8):
            byte_chunk = original_bits[i:i+8]
            if len(byte_chunk) == 8:
                decrypted_bytes.append(int("".join(map(str, byte_chunk)), 2))
                
        # 7. Final safe string translation
        return decrypted_bytes.decode('utf-8', errors='ignore').strip('\0')
        
    except Exception as e:
        return f"Jumble Decrypt Error: {str(e)}"