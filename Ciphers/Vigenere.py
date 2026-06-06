def encrypt(text, key):
    """
    Encrypts text using a keyword to determine varying Caesar shifts.
    """
    result = ""
    # Ensure the key is all letters and uppercase for math consistency
    key = "".join(filter(str.isalpha, key)).upper()
    if not key:
        return text # Return original if key is empty/invalid
    
    key_index = 0
    for char in text:
        if char.isalpha():
            # Get shift amount from current key letter (A=0, B=1, etc.)
            shift = ord(key[key_index % len(key)]) - ord('A')
            
            start = ord('A') if char.isupper() else ord('a')
            new_char = chr(start + (ord(char) - start + shift) % 26)
            result += new_char
            
            # Only move to the next key letter if we actually encrypted a character
            key_index += 1
        else:
            result += char
    return result

def decrypt(text, key):
    """
    Decrypts by reversing the keyword shifts.
    """
    key = "".join(filter(str.isalpha, key)).upper()
    if not key:
        return text
        
    result = ""
    key_index = 0
    for char in text:
        if char.isalpha():
            # To decrypt, we subtract the shift instead of adding it
            shift = ord(key[key_index % len(key)]) - ord('A')
            
            start = ord('A') if char.isupper() else ord('a')
            new_char = chr(start + (ord(char) - start - shift) % 26)
            result += new_char
            
            key_index += 1
        else:
            result += char
    return result