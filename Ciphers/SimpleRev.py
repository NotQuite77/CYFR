def encrypt(text, key=None):
    """
    Completely reverses the string.
    'Cipher' becomes 'rehpiC'
    """
    # Using Python slicing to reverse the string
    return text[::-1]

def decrypt(text, key=None):
    """
    Reversing a reversed string returns it to original.
    """
    return text[::-1]