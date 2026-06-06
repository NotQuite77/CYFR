def encrypt(text, key=None):
    """
    Shifts letters by 13 positions. 
    A <-> N, B <-> O, etc.
    """
    result = ""
    for char in text:
        if char.isalpha():
            # Determine if uppercase or lowercase starting point
            start = ord('A') if char.isupper() else ord('a')
            # Shift by 13 and wrap around the 26-letter alphabet
            new_char = chr(start + (ord(char) - start + 13) % 26)
            result += new_char
        else:
            # Keep spaces, numbers, and punctuation as they are
            result += char
    return result

def decrypt(text, key=None):
    """
    In Rot13, encrypting a second time results in the original text.
    """
    return encrypt(text, key)