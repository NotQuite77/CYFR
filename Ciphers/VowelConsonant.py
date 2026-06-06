import random

def encrypt(plaintext, key=None):
    try:
        if not plaintext:
            return ""

        # 1. Convert secret message into bits (1s and 0s)
        binary_secret = ''.join(format(ord(c), '08b') for c in plaintext)
        
        # 2. Vocabulary pools split by what letter they start with (Vowel vs Consonant)
        # This allows us to assemble sentences word-by-word matching the bit pattern.
        vowels = "aeiouAEIOU"
        
        vowel_words = ["apple", "orange", "index", "update", "error", "online", "object", "entry", "output", "image"]
        consonant_words = ["data", "system", "code", "file", "lock", "save", "core", "test", "main", "loop", "node", "link"]
        
        # Connectors to make the text flow better
        vowel_connectors = ["is", "in", "at", "on", "and", "under", "after"]
        consonant_connectors = ["the", "this", "that", "with", "from", "through", "before"]

        result_words = []
        bit_idx = 0
        
        # 3. Match each bit to the STARTING letter type of a word
        while bit_idx < len(binary_secret):
            current_bit = binary_secret[bit_idx]
            
            if current_bit == '0':
                # Needs a word starting with a VOWEL
                word = random.choice(vowel_words) if bit_idx % 2 == 0 else random.choice(vowel_connectors)
            else:
                # Needs a word starting with a CONSONANT
                word = random.choice(consonant_words) if bit_idx % 2 == 0 else random.choice(consonant_connectors)
                
            result_words.append(word)
            bit_idx += 1
            
            # Periodically add periods to format sentences naturally
            if bit_idx % 6 == 0 and bit_idx < len(binary_secret):
                result_words[-1] += "."

        if not result_words[-1].endswith("."):
            result_words[-1] += "."

        # Re-capitalize sentence beginnings for human realism
        paragraph = " ".join(result_words)
        sentences = paragraph.split(". ")
        capitalized_sentences = [s.strip().capitalize() for s in sentences if s.strip()]
        
        return ". ".join(capitalized_sentences) + "."
        
    except Exception as e:
        return f"VowelConsonant Error: {str(e)}"

def decrypt(ciphertext, key=None):
    try:
        words = ciphertext.split()
        extracted_bits = []
        vowels = "aeiouAEIOU"
        
        # 1. Scan the first letter of every word
        for word in words:
            # Clean punctuation off the word to get the true starting letter
            clean_word = "".join([c for c in word if c.isalpha()])
            
            if clean_word:
                first_letter = clean_word[0]
                
                # Vowel = 0, Consonant = 1
                if first_letter in vowels:
                    extracted_bits.append('0')
                else:
                    extracted_bits.append('1')
                    
        if not extracted_bits:
            return "Error: No hidden linguistic signatures found."
            
        # 2. Reconstruct bits into 8-bit characters
        bit_string = "".join(extracted_bits)
        secret_chars = []
        
        for i in range(0, len(bit_string), 8):
            byte = bit_string[i:i+8]
            if len(byte) == 8:
                if byte == "00000000":
                    break
                secret_chars.append(chr(int(byte, 2)))
                
        return "".join(secret_chars)
    except Exception as e:
        return f"Error: VowelConsonant parsing failed ({str(e)})"