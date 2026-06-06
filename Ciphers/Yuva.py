import hashlib

def generate_shift_stream(key_str, length):
    # Create a long, deterministic stream of numeric shift offsets from the master key
    shifts = []
    counter = 0
    h = hashlib.sha256(str(key_str).encode()).digest()
    
    while len(shifts) < length:
        # Mutate the seed natively using a counter byte loop
        seed = hashlib.sha256(h + bytes([counter % 256])).digest()
        for byte in seed:
            # Convert bytes to shift values between 1 and 94
            shifts.append((byte % 94) + 1)
        counter += 1
        
    return shifts[:length]

def encrypt(text, key):
    try:
        if not text: return ""
        shifts = generate_shift_stream(key, len(text))
        
        result = []
        for idx, char in enumerate(text):
            ord_val = ord(char)
            
            # Target the printable ASCII range safely (space 32 to tilde 126)
            if 32 <= ord_val <= 126:
                shift = shifts[idx]
                # Rotate the character forward within the 95-character printable ASCII block
                new_ord = 32 + ((ord_val - 32 + shift) % 95)
                result.append(chr(new_ord))
            else:
                # Keep unicode characters or systemic line breaks perfectly intact
                result.append(char)
                
        return "".join(result)
    except Exception as e:
        return f"Yuva Error: {str(e)}"

def decrypt(text, key):
    try:
        if not text: return ""
        shifts = generate_shift_stream(key, len(text))
        
        result = []
        for idx, char in enumerate(text):
            ord_val = ord(char)
            
            if 32 <= ord_val <= 126:
                shift = shifts[idx]
                # Reverse the math by subtracting the shift offset backward
                new_ord = 32 + ((ord_val - 32 - shift) % 95)
                result.append(chr(new_ord))
            else:
                result.append(char)
                
        return "".join(result)
    except Exception as e:
        return f"Yuva Decrypt Error: {str(e)}"