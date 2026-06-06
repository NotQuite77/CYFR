import math

def encrypt(text, key):
    # 1. Clean the text up front to establish a true length tracking baseline
    text = text.replace(" ", "")
    if not text:
        return ""

    # 2. Convert key to a number safely
    try:
        n_rails = int(key)
    except (ValueError, TypeError):
        n_rails = sum(ord(char) for char in str(key))
    
    # 3. PIPELINE FIX: Fit the number of rails inside the message boundaries
    # Using modulo prevents n_rails from being larger than the text length.
    if n_rails >= len(text) and len(text) > 2:
        n_rails = (n_rails % (len(text) - 1)) + 2
        
    if n_rails < 2:
        n_rails = 2
        
    if n_rails >= len(text):
        return text

    # 4. Create the zigzag pattern
    fence = [[] for _ in range(n_rails)]
    rail = 0
    direction = 1

    for char in text:
        fence[rail].append(char)
        
        # EDGE-CASE FIX: Check boundaries BEFORE adding direction to avoid indexing stalls
        if n_rails > 1:
            if rail == n_rails - 1:
                direction = -1
            elif rail == 0 and len(fence[0]) > 1: # Only bounce back up after the first drop
                direction = 1
                
        rail += direction
            
    return "".join(["".join(r) for r in fence])

def decrypt(text, key):
    text = text.strip()
    if not text:
        return ""

    try:
        n_rails = int(key)
    except (ValueError, TypeError):
        n_rails = sum(ord(char) for char in str(key))
    
    # PIPELINE FIX: Match the identical modulo scaling used during encryption
    if n_rails >= len(text) and len(text) > 2:
        n_rails = (n_rails % (len(text) - 1)) + 2
        
    if n_rails < 2:
        n_rails = 2
        
    if n_rails >= len(text):
        return text

    # 1. Determine the 'shape' of the fence using indices
    pattern = [[] for _ in range(n_rails)]
    rail = 0
    direction = 1

    for i in range(len(text)):
        pattern[rail].append(i)
        if n_rails > 1:
            if rail == n_rails - 1:
                direction = -1
            elif rail == 0 and len(pattern[0]) > 1:
                direction = 1
        rail += direction

    # 2. Fill the pattern with the actual characters
    result = [''] * len(text)
    text_idx = 0
    for r in range(n_rails):
        for pos in pattern[r]:
            if text_idx < len(text):
                result[pos] = text[text_idx]
                text_idx += 1
            
    return "".join(result)