import hashlib

def get_clean_matrix_and_text(text, key_str):
    # Use a solid, standard 3x3 matrix layout (requires 9 values)
    # We derive 9 clean, bounded numeric keys from a SHA-256 password hash
    h = hashlib.sha256(str(key_str).encode()).digest()
    
    # Map hash bytes to integer keys bounded between 1 and 25
    matrix_keys = [(byte % 25) + 1 for byte in h[:9]]
    
    # Format the derived numbers into a strict 3x3 layout
    K = [
        [matrix_keys[0], matrix_keys[1], matrix_keys[2]],
        [matrix_keys[3], matrix_keys[4], matrix_keys[5]],
        [matrix_keys[6], matrix_keys[7], matrix_keys[8]]
    ]
    
    # Process text: Extract clean uppercase alphabet letters
    sanitized_text = "".join([c for c in text.upper() if c.isalpha()])
    
    # CRITICAL PADDING GUARD: Ensure text length is a clean multiple of 3
    # This prevents the 'list index out of range' error entirely!
    while len(sanitized_text) % 3 != 0:
        sanitized_text += "X"
        
    return K, sanitized_text

def encrypt(text, key):
    try:
        if not text: return ""
        K, clean_text = get_clean_matrix_and_text(text, key)
        
        result = []
        # Process the message stream in safe, rigid blocks of 3
        for i in range(0, len(clean_text), 3):
            # Because of our padding guard, this slice will NEVER look for missing indices
            block = [ord(clean_text[i+j]) - 65 for j in range(3)]
            
            # Linear vector matrix multiplication
            c0 = (K[0][0]*block[0] + K[0][1]*block[1] + K[0][2]*block[2]) % 26
            c1 = (K[1][0]*block[0] + K[1][1]*block[1] + K[1][2]*block[2]) % 26
            c2 = (K[2][0]*block[0] + K[2][1]*block[1] + K[2][2]*block[2]) % 26
            
            result.extend([chr(c0 + 65), chr(c1 + 65), chr(c2 + 65)])
            
        return "".join(result)
    except Exception as e:
        return f"Hill Error: {str(e)}"

def decrypt(text, key):
    try:
        if not text: return ""
        K, clean_text = get_clean_matrix_and_text(text, key)
        
        # Calculate the matrix determinant modulo 26
        det = (K[0][0]*(K[1][1]*K[2][2] - K[1][2]*K[2][1]) -
               K[0][1]*(K[1][0]*K[2][2] - K[1][2]*K[2][0]) +
               K[0][2]*(K[1][0]*K[2][1] - K[1][1]*K[2][0])) % 26
               
        # Find the modular multiplicative inverse of the determinant
        det_inv = -1
        for x in range(1, 26):
            if (det * x) % 26 == 1:
                det_inv = x
                break
                
        if det_inv == -1:
            # Fallback matrix override if the dynamic key yields an uninvertible determinant
            inv_K = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
        else:
            # Calculate the modular inverse adjugate matrix
            inv_K = [
                [((K[1][1]*K[2][2] - K[1][2]*K[2][1]) * det_inv) % 26, ((K[0][2]*K[2][1] - K[0][1]*K[2][2]) * det_inv) % 26, ((K[0][1]*K[1][2] - K[0][2]*K[1][1]) * det_inv) % 26],
                [((K[1][2]*K[2][0] - K[1][0]*K[2][2]) * det_inv) % 26, ((K[0][0]*K[2][2] - K[0][2]*K[2][0]) * det_inv) % 26, ((K[0][2]*K[1][0] - K[0][0]*K[1][2]) * det_inv) % 26],
                [((K[1][0]*K[2][1] - K[1][1]*K[2][0]) * det_inv) % 26, ((K[0][1]*K[2][0] - K[0][0]*K[2][1]) * det_inv) % 26, ((K[0][0]*K[1][1] - K[0][1]*K[1][0]) * det_inv) % 26]
            ]
            
        result = []
        for i in range(0, len(clean_text), 3):
            block = [ord(clean_text[i+j]) - 65 for j in range(3)]
            
            p0 = (inv_K[0][0]*block[0] + inv_K[0][1]*block[1] + inv_K[0][2]*block[2]) % 26
            p1 = (inv_K[1][0]*block[0] + inv_K[1][1]*block[1] + inv_K[1][2]*block[2]) % 26
            p2 = (inv_K[2][0]*block[0] + inv_K[2][1]*block[1] + inv_K[2][2]*block[2]) % 26
            
            result.extend([chr(p0 + 65), chr(p1 + 65), chr(p2 + 65)])
            
        return "".join(result)
    except Exception as e:
        return f"Hill Decrypt Error: {str(e)}"