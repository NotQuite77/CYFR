import base64

def encrypt(text, key=None):
    """
    Encodes text into Base64 format.
    """
    # Convert string to bytes
    text_bytes = text.encode('utf-8')
    # Encode to base64 bytes
    base64_bytes = base64.b64encode(text_bytes)
    # Convert back to string for the system to handle
    return base64_bytes.decode('utf-8')

def decrypt(text, key=None):
    """
    Decodes Base64 string back into original text.
    """
    try:
        # Convert string to bytes
        base64_bytes = text.encode('utf-8')
        # Decode base64
        sample_string_bytes = base64.b64decode(base64_bytes)
        # Convert back to string
        return sample_string_bytes.decode('utf-8')
    except Exception:
        # If the input isn't valid Base64, return as is (prevents crashing)
        return text