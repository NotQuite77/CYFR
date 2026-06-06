import hashlib

def generate_keyed_alphabet(key_str):
    # Standard uppercase baseline
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    
    # Create a unique scrambled alphabet from the key
    clean_key = ""
    for char in key_str.upper():
        if char in alphabet and char not in clean_key:
            clean_key += char
            
    # Fill out the remaining slots with the rest of the alphabet
    keyed_alphabet = clean_key
    for char in alphabet:
        if char not in keyed_alphabet:
            keyed_alphabet += char
            
    return keyed_alphabet

def encrypt(text, key):
    try:
        if not text: return ""
        
        # Quagmire III relies on a keyed alphabet base
        pt_alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ" # Plaintext lookup layout
        ct_alphabet = generate_keyed_alphabet(str(key)) # Scrambled cipher layout
        
        # Use a secondary derivation of the key as our row indicator stream
        indicator_hash = hashlib.md5(str(key).encode()).hexdigest().upper()
        indicator_stream = "".join([c for c in indicator_hash if c.isalpha()])
        if not indicator_stream:
            indicator_stream = "KHAZAD" # Fallback indicator string
            
        result = []
        indicator_idx = 0
        
        for char in text.upper():
            if char.isalpha():
                # 1. Find the position of the plaintext char in standard alphabet
                pt_pos = pt_alphabet.index(char)
                
                # 2. Get the row indicator character for this step
                ind_char = indicator_stream[indicator_idx % len(indicator_stream)]
                
                # 3. Find where the indicator character sits in the scrambled cipher alphabet
                shift_offset = ct_alphabet.index(ind_char)
                
                # 4. Extract the encrypted character using the shifted matrix index
                ct_pos = (pt_pos + shift_offset) % 26
                result.append(ct_alphabet[ct_pos])
                
                indicator_idx += 1
            else:
                # Keep spaces, punctuation, and numbers intact without breaking
                result.append(char)
                
        return "".join(result)
    except Exception as e:
        return f"Quagmire Error: {str(e)}"

def decrypt(text, key):
    try:
        if not text: return ""
        
        pt_alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        ct_alphabet = generate_keyed_alphabet(str(key))
        
        indicator_hash = hashlib.md5(str(key).encode()).hexdigest().upper()
        indicator_stream = "".join([c for c in indicator_hash if c.isalpha()])
        if not indicator_stream:
            indicator_stream = "KHAZAD"
            
        result = []
        indicator_idx = 0
        
        for char in text.upper():
            if char.isalpha():
                # 1. Find the row indicator shift offset
                ind_char = indicator_stream[indicator_idx % len(indicator_stream)]
                shift_offset = ct_alphabet.index(ind_char)
                
                # 2. Locate where the cipher character sits in the scrambled alphabet
                ct_pos = ct_alphabet.index(char)
                
                # 3. Reverse the shift operation mathematically
                pt_pos = (ct_pos - shift_offset) % 26
                result.append(pt_alphabet[pt_pos])
                
                indicator_idx += 1
            else:
                result.append(char)
                
        return "".join(result)
    except Exception as e:
        return f"Quagmire Decrypt Error: {str(e)}"