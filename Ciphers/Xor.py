def encrypt(text, key):
    """
    XORs the text and then converts it to HEX so it is safe to pass
    to other ciphers in your sequence.
    """
    if not key:
        return text
        
    key_ints = [ord(c) for c in str(key)]
    xor_result = ""
    
    for i in range(len(text)):
        char_code = ord(text[i])
        key_code = key_ints[i % len(key_ints)]
        # ^ is the XOR operator
        xor_result += chr(char_code ^ key_code)
    
    # Convert the "messy" XOR result into a clean Hex string
    # This prevents the 'blank result' issue.
    return xor_result.encode('utf-8').hex()

def decrypt(text, key):
    """
    Converts Hex back to bytes, then XORs it back to original text.
    """
    if not key:
        return text
        
    try:
        # 1. Convert the Hex string back into the "messy" characters
        bytes_obj = bytes.fromhex(text)
        messy_text = bytes_obj.decode('utf-8')
        
        # 2. XOR it again with the same key to get original text
        key_ints = [ord(c) for c in str(key)]
        result = ""
        for i in range(len(messy_text)):
            char_code = ord(messy_text[i])
            key_code = key_ints[i % len(key_ints)]
            result += chr(char_code ^ key_code)
        return result
    except Exception:
        # If decryption fails (e.g., input wasn't hex), return text as is
        return text