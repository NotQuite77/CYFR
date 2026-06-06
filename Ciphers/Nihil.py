import hashlib

def generate_polybius_grid(key_str):
    # Standard 5x5 alphabet grid baseline (merging J into I)
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
    
    # Create a unique key sequence based on the user's password
    clean_key = ""
    for char in key_str.upper():
        if char == 'J': char = 'I'
        if char in alphabet and char not in clean_key:
            clean_key += char
            
    # Fill out the rest of the grid with the remaining alphabet letters
    grid_string = clean_key
    for char in alphabet:
        if char not in grid_string:
            grid_string += char
            
    # Build coordinate lookup dictionaries
    # Row and Column values span from 1 to 5
    char_to_num = {}
    num_to_char = {}
    for idx, char in enumerate(grid_string):
        row = (idx // 5) + 1
        col = (idx % 5) + 1
        coord = row * 10 + col  # e.g., Row 2, Col 3 becomes the integer 23
        char_to_num[char] = coord
        num_to_char[coord] = char
        
    return char_to_num, num_to_char

def encrypt(text, key):
    try:
        if not text: return ""
        char_to_num, _ = generate_polybius_grid(key)
        
        # 1. Convert plaintext to Polybius coordinates
        plain_coords = []
        for char in text.upper():
            if char == 'J': char = 'I'
            if char in char_to_num:
                plain_coords.append(char_to_num[char])
                
        # 2. Convert the key itself into a looping keystream coordinate array
        key_coords = []
        for char in str(key).upper():
            if char == 'J': char = 'I'
            if char in char_to_num:
                key_coords.append(char_to_num[char])
                
        if not key_coords:
            key_coords = [11] # Fallback if key has no alphabet characters
            
        # 3. Add plain coordinates and key coordinates together mathematically
        cipher_nums = []
        for idx, p_coord in enumerate(plain_coords):
            k_coord = key_coords[idx % len(key_coords)]
            cipher_nums.append(str(p_coord + k_coord))
            
        # Join with spaces for standard cipher presentation output
        return " ".join(cipher_nums)
    except Exception as e:
        return f"Nihilist Error: {str(e)}"

def decrypt(text, key):
    try:
        if not text: return ""
        char_to_num, num_to_char = generate_polybius_grid(key)
        
        # Parse the space-separated number string back into an array of integers
        cipher_nums = [int(num) for num in text.split() if num.isdigit()]
        
        # Re-derive the looping key coordinate sequence
        key_coords = []
        for char in str(key).upper():
            if char == 'J': char = 'I'
            if char in char_to_num:
                key_coords.append(char_to_num[char])
                
        if not key_coords:
            key_coords = [11]
            
        # Subtract the key coordinates out to reveal the original Polybius locations
        decrypted_chars = []
        for idx, c_num in enumerate(cipher_nums):
            k_coord = key_coords[idx % len(key_coords)]
            plain_coord = c_num - k_coord
            
            if plain_coord in num_to_char:
                decrypted_chars.append(num_to_char[plain_coord])
            else:
                decrypted_chars.append("?") # Fallback flag for broken bits
                
        return "".join(decrypted_chars)
    except Exception as e:
        return f"Nihilist Decrypt Error: {str(e)}"