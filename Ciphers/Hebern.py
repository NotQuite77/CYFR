import hashlib

def get_rotor(key):
    # Create a scrambled alphabet based on your Master Key
    alphabet = list("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789 ./")
    seed = int(hashlib.sha256(str(key).encode()).hexdigest(), 16)
    
    # Deterministic shuffle using the seed
    import random
    rng = random.Random(seed)
    scrambled = alphabet[:]
    rng.shuffle(scrambled)
    return alphabet, scrambled

def encrypt(text, key):
    try:
        base_alpha, rotor = get_rotor(key)
        n = len(base_alpha)
        result = ""
        
        for i, char in enumerate(text):
            if char in base_alpha:
                # Find current index
                idx = base_alpha.index(char)
                # Shift by 'i' (the rotor rotation)
                shifted_idx = (idx + i) % n
                # Substitute and add to result
                result += rotor[shifted_idx]
            else:
                result += char
        return result
    except Exception as e:
        return f"Hebern Error: {str(e)}"

def decrypt(text, key):
    try:
        base_alpha, rotor = get_rotor(key)
        n = len(base_alpha)
        result = ""
        
        for i, char in enumerate(text):
            if char in rotor:
                # Find where it is in the scrambled rotor
                idx = rotor.index(char)
                # Reverse the shift
                orig_idx = (idx - i) % n
                # Get the original character
                result += base_alpha[orig_idx]
            else:
                result += char
        return result
    except:
        return "Hebern Decrypt Error"