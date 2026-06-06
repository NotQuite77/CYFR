def encrypt(text, key=None): # Key is ignored in Atbash but kept for the pipeline
    result = ""
    for char in text:
        if char.isalpha():
            if char.isupper():
                # Flip relative to 'A' (65) and 'Z' (90)
                result += chr(90 - (ord(char) - 65))
            else:
                # Flip relative to 'a' (97) and 'z' (122)
                result += chr(122 - (ord(char) - 97))
        else:
            # If it's a space, number, or symbol, just keep it!
            result += char
    return result

def decrypt(text, key=None):
    # Atbash is its own inverse, so we just run encrypt again
    return encrypt(text)