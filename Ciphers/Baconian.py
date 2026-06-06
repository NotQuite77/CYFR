# The classic 5-bit Baconian alphabet mapping (A and B combinations)
BACON_MAP = {
    'A': 'aaaaa', 'B': 'aaaab', 'C': 'aaaba', 'D': 'aaabb', 'E': 'aabaa',
    'F': 'aabab', 'G': 'aabba', 'H': 'aabbb', 'I': 'abaaa', 'J': 'abaab',
    'K': 'ababa', 'L': 'ababb', 'M': 'abbaa', 'N': 'abbab', 'O': 'abbba',
    'P': 'abbbb', 'Q': 'baaaa', 'R': 'baaab', 'S': 'baaba', 'T': 'baabb',
    'U': 'babaa', 'V': 'babab', 'W': 'babba', 'X': 'babbb', 'Y': 'bbaaa',
    'Z': 'bbaab'
}

# Reverse lookup for quick decryption decoding
REVERSE_BACON_MAP = {v: k for k, v in BACON_MAP.items()}

def encrypt(plaintext, key=None):
    try:
        if not plaintext:
            return ""

        # 1. Clean the secret text and convert it to Baconian A/B strings
        secret_clean = "".join([c.upper() for c in plaintext if c.isalpha()])
        bacon_stream = ""
        
        for char in secret_clean:
            bacon_stream += BACON_MAP.get(char, "aaaaa") # Default to 'A' if unknown character
            
        # 2. YOUR CUSTOM COVER SENTENCES - Change these to whatever you want!
        # Keep them lowercase so the script has clean room to apply the capitalization masks.
        sentence_pool = [
               "All paths lead to the same destination.", "Always look ahead for new horizons.", "Action speaks louder than empty words.",
    "Before you leave, check the parameters.", "Behind the curtain lies the true sequence.", "Books contain keys to forgotten vaults.",
    "Codes are meant to be broken cleanly.", "Current data streams look completely stable.", "Capture the signal before it fades away.",
    "Data leaks can expose critical pipelines.", "Do not alter the master key variables.", "Down in the server room, fans are buzzing.",
    "Every execution loop must have an exit.", "Encryption shields your data from observers.", "Enter the passkey to open the terminal.",
    "Files are fully synchronized across systems.", "Find the hidden offset inside the string.", "For security reasons, clear the output logs.",
    "Global shields are actively monitoring ports.", "Go through the sequence layer by layer.", "Gibberish text usually means a wrong key.",
    "Hidden markers are buried in plain text.", "How did the pipeline layout get misaligned?", "Hello from the other side of the network.",
    "Incoming packets are cleanly formatted.", "Initialize the dynamic variables right now.", "Invalid arguments will trigger a crash flag.",
    "Jumbled letters make parsing quite difficult.", "Join the strings back into a unified block.", "Just execute the hub handler function.",
    "Keys must be kept strictly confidential.", "Keep tracking the background terminal logs.", "Knowledge is the ultimate security layer.",
    "Layout changes might break widget placement.", "Lines of code are executing sequentially.", "Look down the margin to read the secret.",
    "Matrix operations require specific matching.", "Multi-layered systems are highly robust.", "Messages travel across transport pipelines.",
    "Network routing handles the data packaging.", "No errors were detected during compilation.", "Null pointers will drop the thread instantly.",
    "Output displays the final resulting string.", "Operational integrity remains at maximum.", "Only authorized keys can pass the boundary.",
    "Padding blocks ensure proper data sizes.", "Pipeline execution finished successfully.", "Python scripts run seamlessly in backgrounds.",
    "Queries are fetching data blocks rapidly.", "Quitting early resets the entire system.", "Quickly patch the encoding layout leak.",
    "Raw bytes must be converted to strings.", "Run the standalone test modules first.", "Reverse the sequence string to decrypt it.",
    "Symmetric encryption is incredibly fast.", "Sequence letters determine active ciphers.", "Strip trailing whitespaces from text inputs.",
    "Tracking algorithms are fully operational.", "The master key bypasses the layout shield.", "Type your secret message inside the box.",
    "Unicode characters can bypass standard rules.", "Update your core dependencies regularly.", "Unknown sequence commands are discarded.",
    "Variables are stored inside memory blocks.", "Verify the integrity of the data stream.", "Vigenere math relies on alphabet shifting.",
    "Watch out for hidden padding artifacts.", "Widgets are rendering perfectly on screens.", "Wrong keys will generate absolute garbage.",
    "Xor operations process data bit by bit.", "XTEA handles 64-bit blocks with ease.", "X-ray scans revealed structural layout bugs.",
    "Your encryption workspace is ready.", "Yield parameters before dropping loops.", "Yesterday all functions compiled cleanly.",
    "Zero-width spaces hide strings completely.", "Zigzag patterns form the railfence shape.", "Zone security configurations are locked down."
        ]
        
        # 3. Assemble a long enough paragraph to hold the AB stream
        cover_text_list = []
        pool_idx = 0
        total_letters = 0
        
        while total_letters < len(bacon_stream):
            current_sentence = sentence_pool[pool_idx % len(sentence_pool)]
            cover_text_list.append(current_sentence)
            total_letters += sum(1 for c in current_sentence if c.isalpha())
            pool_idx += 1
            
        cover_text = " ".join(cover_text_list)
        
        # 4. Hide the Baconian stream using Capitalization
        result_chars = []
        bacon_idx = 0
        
        for char in cover_text:
            if bacon_idx < len(bacon_stream) and char.isalpha():
                current_bit = bacon_stream[bacon_idx]
                
                # 'a' = lowercase, 'b' = uppercase
                if current_bit == 'b':
                    result_chars.append(char.upper())
                else:
                    result_chars.append(char.lower())
                bacon_idx += 1
            else:
                result_chars.append(char)
                
        return "".join(result_chars)
        
    except Exception as e:
        return f"Baconian Error: {str(e)}"

def decrypt(ciphertext, key=None):
    try:
        extracted_ab = []
        
        # 1. Gather all capitalization states from the text string
        for char in ciphertext:
            if char.isalpha():
                # uppercase = b, lowercase = a
                extracted_ab.append('b' if char.isupper() else 'a')
                
        if not extracted_ab:
            return "Error: No hidden Baconian markers found in this layout."
            
        ab_string = "".join(extracted_ab)
        secret_chars = []
        
        # 2. Slice the AB string into distinct 5-bit chunks and look them up
        for i in range(0, len(ab_string), 5):
            chunk = ab_string[i:i+5]
            if len(chunk) == 5:
                decoded_char = REVERSE_BACON_MAP.get(chunk, "")
                if decoded_char:
                    secret_chars.append(decoded_char)
                else:
                    # If we hit an unmapped chunk, it means we reached the end of the secret padding
                    break
                    
        return "".join(secret_chars)
    except Exception as e:
        return f"Error: Baconian parsing failed ({str(e)})"