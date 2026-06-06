import string

def encrypt(plaintext, key=None):
    try:
        if not plaintext:
            return ""

        # 1. Convert secret message into bits (1s and 0s)
        binary_secret = ''.join(format(ord(c), '08b') for c in plaintext)
        
        # 2. MASSIVE COVER WORD DICTIONARY (Categorized strictly by letter length count)
        # EVEN LETTER LENGTH POOLS (Represents Bit '0')
        even_pool = [
            # 2 Letters
            "is", "it", "to", "on", "at", "by", "an", "so", "me", "my", "we", "he", "do", "no", "up",
            # 4 Letters
            "that", "this", "fine", "good", "data", "file", "code", "lock", "open", "save", "core", "test",
            "team", "task", "work", "time", "plan", "view", "make", "here", "read", "load", "true", "date",
            "user", "pass", "send", "sync", "main", "mode", "text", "page", "size", "byte", "bits", "node",
            "easy", "fast", "slow", "high", "long", "chat", "loop", "grid", "menu", "icon", "font", "link",
            "well", "sure", "nice", "cool", "back", "left", "keep", "take", "show", "find", "give", "call",
            # 6 Letters
            "system", "cipher", "studio", "secure", "output", "format", "update", "source", "module", "script",
            "window", "widget", "button", "screen", "layout", "design", "online", "access", "server", "client",
            "report", "result", "status", "review", "change", "create", "delete", "remove", "insert", "finish",
            "simple", "modern", "robust", "fluent", "active", "stable", "unique", "global", "hidden", "secret"
        ]
        
        even_connectors = [
            # 4 Letters
            "with", "from", "into", "over", "then", "more", "also", "just", "even", "such", "than", "upon",
            # 6 Letters
            "before", "during", "either", "unless", "except", "within", "behind", "across", "beyond", "toward"
        ]

        # ODD LETTER LENGTH POOLS (Represents Bit '1')
        odd_pool = [
            # 3 Letters
            "the", "and", "for", "but", "not", "you", "all", "any", "new", "run", "set", "get", "key", "box", "log",
            # 5 Letters
            "apple", "looks", "great", "check", "input", "write", "print", "clear", "setup", "route", "bytes",
            "frame", "label", "panel", "image", "graph", "chart", "table", "index", "value", "field", "range",
            "count", "total", "phase", "stage", "event", "click", "hover", "press", "enter", "space", "shift",
            "ready", "valid", "error", "fault", "alert", "alarm", "watch", "timer", "clock", "brief", "short",
            "basic", "smart", "quick", "clean", "fresh", "stuck", "wrong", "right", "close", "start", "begin",
            # 7 Letters
            "process", "library", "dynamic", "network", "element", "console", "sidebar", "toolbar", "heading", "graphic",
            "project", "version", "history", "profile", "account", "setting", "feature", "options", "display", "message",
            "preview", "request", "respond", "receive", "extract", "convert", "parsing", "storage", "utility", "toolkit"
        ]
        
        odd_connectors = [
            # 5 Letters
            "about", "under", "after", "their", "there", "which", "while", "where", "since", "until", "among", "above",
            # 7 Letters",
            "through", "against", "between", "whereas", "without", "despite", "besides", "forward", "towards", "anytime"
        ]

        result_words = []
        bit_idx = 0
        
        # 3. Construct sentences dynamically based on the binary secret layout
        while bit_idx < len(binary_secret):
            current_bit = binary_secret[bit_idx]
            
            # Use a mixing hash formula so sequential loops jump forward across the expansive list sizes
            selector_hash = (bit_idx * 31 + 17)
            
            if current_bit == '0':
                # Needs an EVEN length word
                if bit_idx % 4 != 0:
                    word = even_pool[selector_hash % len(even_pool)]
                else:
                    word = even_connectors[selector_hash % len(even_connectors)]
            else:
                # Needs an ODD length word
                if bit_idx % 4 != 0:
                    word = odd_pool[selector_hash % len(odd_pool)]
                else:
                    word = odd_connectors[selector_hash % len(odd_connectors)]
                    
            result_words.append(word)
            bit_idx += 1
            
            # Periodically drop sentence breaks to maintain paragraph structuring looks
            if bit_idx % 8 == 0 and bit_idx < len(binary_secret):
                result_words[-1] += "."
                
        # Close the final sentence cleanly
        if not result_words[-1].endswith("."):
            result_words[-1] += "."
            
        # Capitalize the first letter of sentences dynamically
        paragraph = " ".join(result_words)
        sentences = paragraph.split(". ")
        capitalized_sentences = [s.strip().capitalize() for s in sentences if s.strip()]
        
        return ". ".join(capitalized_sentences) + "."
        
    except Exception as e:
        return f"WordCount Error: {str(e)}"

def decrypt(ciphertext, key=None):
    try:
        # 1. Split text into individual words
        raw_words = ciphertext.split()
        extracted_bits = []
        
        for word in raw_words:
            # 2. Strip off any punctuation to get the strict letter count
            clean_word = "".join([c for c in word if c.isalpha()])
            
            if clean_word:
                # Even length = 0, Odd length = 1
                if len(clean_word) % 2 == 0:
                    extracted_bits.append('0')
                else:
                    extracted_bits.append('1')
                    
        if not extracted_bits:
            return "Error: No hidden word-length data found in this text."
            
        # 3. Reconstruct the bits back into standard 8-bit characters
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
        return f"Error: WordCount parsing failed ({str(e)})"