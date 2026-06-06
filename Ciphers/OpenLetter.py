import random

def encrypt(plaintext, key=None):
    try:
        if not plaintext:
            return ""

        # 1. Clean the secret message
        secret_clean = "".join([c.upper() for c in plaintext if c.isalpha()])
        if not secret_clean:
            return "Error: Message must contain letters to encrypt."

        # Our unique marker: 'tt' followed by the secret letter
        # This guarantees the decryptor never reads accidental 't's in normal words!
        trigger_prefix = 'tt'
        
        # 2. Your high-fidelity, professional sentence pool
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

        result_sentences = []
        
        # 3. Step through your secret letters and append a clean cover sentence + the hidden marker word
        for target_char in secret_clean:
            # Pick a random sentence to act as camouflage 
            base_sentence = random.choice(sentence_pool)
            result_sentences.append(base_sentence)
            
            # Inject our targeted marker word right after it (e.g., "tta", "tto", etc.)
            # To a casual reader, it looks like a slight typo or an artifact, completely blending in.
            hidden_word = f"{trigger_prefix}{target_char.lower()}"
            result_sentences.append(hidden_word)
            
        return " ".join(result_sentences)
        
    except Exception as e:
        return f"OpenLetter Error: {str(e)}"

def decrypt(ciphertext, key=None):
    try:
        words = ciphertext.split()
        secret_chars = []
        
        # 1. Scan word by word
        for word in words:
            clean_word = word.strip(".,!?\"'()").lower()
            
            # 2. If the word explicitly starts with our 'tt' signature, pull the next letter!
            if clean_word.startswith("tt") and len(clean_word) == 3:
                secret_char = clean_word[2]
                if secret_char.isalpha():
                    secret_chars.append(secret_char.upper())
                    
        if not secret_chars:
            return "Error: No hidden Open Letter signatures detected in this layout."
            
        return "".join(secret_chars)
    except Exception as e:
        return f"Error: OpenLetter parsing failed ({str(e)})"