def encrypt(plaintext, key=None):
    try:
        if not plaintext:
            return ""

        # 1. Convert secret message into bits
        binary_secret = ''.join(format(ord(c), '08b') for c in plaintext)
        
        # 2. A pool of unique, natural sentences to build a realistic email/log paragraph
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
        
        # 3. Build a diverse text canvas by looping through unique sentences
        cover_text_list = []
        pool_idx = 0
        total_slots = 0
        
        # Keep adding unique sentences until we have enough 'a' and 'e' slots
        while total_slots < len(binary_secret):
            current_sentence = sentence_pool[pool_idx % len(sentence_pool)]
            cover_text_list.append(current_sentence)
            total_slots += current_sentence.count('e') + current_sentence.count('a')
            pool_idx += 1
            
        cover_text = " ".join(cover_text_list)
        
        # Unicode homoglyphs
        lat_e, cyr_e = "e", "\u0435"
        lat_a, cyr_a = "a", "\u0430"
        
        result_chars = []
        bit_idx = 0
        
        for char in cover_text:
            if bit_idx < len(binary_secret):
                current_bit = binary_secret[bit_idx]
                
                if char == 'e':
                    result_chars.append(cyr_e if current_bit == '1' else lat_e)
                    bit_idx += 1
                elif char == 'a':
                    result_chars.append(cyr_a if current_bit == '1' else lat_a)
                    bit_idx += 1
                else:
                    result_chars.append(char)
            else:
                result_chars.append(char)
            
        return "".join(result_chars)
        
    except Exception as e:
        return f"GhostText Error: {str(e)}"

def decrypt(ciphertext, key=None):
    try:
        cyr_e = "\u0435"
        cyr_a = "\u0430"
        
        extracted_bits = []
        
        # Scan the incoming text stream character by character
        for char in ciphertext:
            if char in ['e', cyr_e]:
                extracted_bits.append('1' if char == cyr_e else '0')
            elif char in ['a', cyr_a]:
                extracted_bits.append('1' if char == cyr_a else '0')
                
        if not extracted_bits:
            return "Error: No hidden text artifacts found in this sentence layout."
            
        bit_string = "".join(extracted_bits)
        secret_chars = []
        
        # Reconstruct the bits back into 8-bit blocks
        for i in range(0, len(bit_string), 8):
            byte = bit_string[i:i+8]
            if len(byte) == 8:
                # If we hit trailing padding blocks or an empty byte, stop decoding
                if byte == "00000000":
                    break
                secret_chars.append(chr(int(byte, 2)))
                
        return "".join(secret_chars)
    except Exception as e:
        return f"Error: GhostText parsing failed ({str(e)})"