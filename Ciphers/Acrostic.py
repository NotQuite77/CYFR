import random

# A pool of dummy sentences to build the paragraph automatically during encryption
DUMMY_SENTENCES = {
    'A': ["All paths lead to the same destination.", "Always look ahead for new horizons.", "Action speaks louder than empty words."],
    'B': ["Before you leave, check the parameters.", "Behind the curtain lies the true sequence.", "Books contain keys to forgotten vaults."],
    'C': ["Codes are meant to be broken cleanly.", "Current data streams look completely stable.", "Capture the signal before it fades away."],
    'D': ["Data leaks can expose critical pipelines.", "Do not alter the master key variables.", "Down in the server room, fans are buzzing."],
    'E': ["Every execution loop must have an exit.", "Encryption shields your data from observers.", "Enter the passkey to open the terminal."],
    'F': ["Files are fully synchronized across systems.", "Find the hidden offset inside the string.", "For security reasons, clear the output logs."],
    'G': ["Global shields are actively monitoring ports.", "Go through the sequence layer by layer.", "Gibberish text usually means a wrong key."],
    'H': ["Hidden markers are buried in plain text.", "How did the pipeline layout get misaligned?", "Hello from the other side of the network."],
    'I': ["Incoming packets are cleanly formatted.", "Initialize the dynamic variables right now.", "Invalid arguments will trigger a crash flag."],
    'J': ["Jumbled letters make parsing quite difficult.", "Join the strings back into a unified block.", "Just execute the hub handler function."],
    'K': ["Keys must be kept strictly confidential.", "Keep tracking the background terminal logs.", "Knowledge is the ultimate security layer."],
    'L': ["Layout changes might break widget placement.", "Lines of code are executing sequentially.", "Look down the margin to read the secret."],
    'M': ["Matrix operations require specific matching.", "Multi-layered systems are highly robust.", "Messages travel across transport pipelines."],
    'N': ["Network routing handles the data packaging.", "No errors were detected during compilation.", "Null pointers will drop the thread instantly."],
    'O': ["Output displays the final resulting string.", "Operational integrity remains at maximum.", "Only authorized keys can pass the boundary."],
    'P': ["Padding blocks ensure proper data sizes.", "Pipeline execution finished successfully.", "Python scripts run seamlessly in backgrounds."],
    'Q': ["Queries are fetching data blocks rapidly.", "Quitting early resets the entire system.", "Quickly patch the encoding layout leak."],
    'R': ["Raw bytes must be converted to strings.", "Run the standalone test modules first.", "Reverse the sequence string to decrypt it."],
    'S': ["Symmetric encryption is incredibly fast.", "Sequence letters determine active ciphers.", "Strip trailing whitespaces from text inputs."],
    'T': ["Tracking algorithms are fully operational.", "The master key bypasses the layout shield.", "Type your secret message inside the box."],
    'U': ["Unicode characters can bypass standard rules.", "Update your core dependencies regularly.", "Unknown sequence commands are discarded."],
    'V': ["Variables are stored inside memory blocks.", "Verify the integrity of the data stream.", "Vigenere math relies on alphabet shifting."],
    'W': ["Watch out for hidden padding artifacts.", "Widgets are rendering perfectly on screens.", "Wrong keys will generate absolute garbage."],
    'X': ["Xor operations process data bit by bit.", "XTEA handles 64-bit blocks with ease.", "X-ray scans revealed structural layout bugs."],
    'Y': ["Your encryption workspace is ready.", "Yield parameters before dropping loops.", "Yesterday all functions compiled cleanly."],
    'Z': ["Zero-width spaces hide strings completely.", "Zigzag patterns form the railfence shape.", "Zone security configurations are locked down."]
}

def encrypt(plaintext, key=None):
    try:
        # 1. Clean the secret message (uppercase and letters only)
        secret = "".join([c.upper() for c in plaintext if c.isalpha()])
        if not secret:
            return "Error: Message must contain letters to form an acrostic."
            
        paragraph_lines = []
        
        # 2. For each letter in your secret, grab a matching dummy sentence
        for char in secret:
            sentences = DUMMY_SENTENCES.get(char, ["Text line formatting placeholder."])
            paragraph_lines.append(random.choice(sentences))
            
        # 3. Join the sentences with actual line breaks to form a vertical list
        return "\n".join(paragraph_lines)
    except Exception as e:
        return f"Acrostic Error: {str(e)}"

def decrypt(ciphertext, key=None):
    try:
        # 1. Split the incoming text paragraph by its line breaks
        lines = ciphertext.strip().split('\n')
        
        secret_chars = []
        for line in lines:
            clean_line = line.strip()
            if clean_line:
                # 2. Grab the very first letter of the line
                secret_chars.append(clean_line[0])
                
        # 3. Smash them together to reveal the secret word
        return "".join(secret_chars)
    except Exception as e:
        return f"Error: Acrostic parsing failed ({str(e)})"