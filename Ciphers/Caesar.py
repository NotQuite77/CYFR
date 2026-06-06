def encrypt(text, key):
    """
    Shifts characters forward. 
    Handles both numeric keys and string keys automatically.
    """
    # Safety Check: Convert string key to a number if necessary
    try:
        shift = int(key)
    except (ValueError, TypeError):
        # If the key is a word (like 'sup'), sum the ASCII values
        # This ensures 'sup' always results in the same numeric shift
        shift = sum(ord(char) for char in str(key))
    
    result = ""
    # Ensure the shift stays within the 26-letter alphabet
    final_shift = shift % 26
    
    for char in text:
        if char.isalpha():
            # Determine if uppercase or lowercase starting point
            start = ord('A') if char.isupper() else ord('a')
            # Shift the character and wrap around
            new_char = chr(start + (ord(char) - start + final_shift) % 26)
            result += new_char
        else:
            # Leave spaces/numbers as they are
            result += char
    return result

def decrypt(text, key):
    """
    To decrypt, we shift backwards by the same amount.
    """
    try:
        shift = int(key)
    except (ValueError, TypeError):
        shift = sum(ord(char) for char in str(key))
        
    # Shifting backwards is just shifting by the negative amount
    return encrypt(text, -shift)