import base64
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

def encrypt(plaintext, key):
    try:
        # 1. Force the key to be exactly 32 bytes using SHA-256 hashing
        hashed_key = hashlib.sha256(key.encode('utf-8')).digest()
        
        # 2. Check if the incoming plaintext is a standard string or raw pipeline data
        # If it's from a previous modern cipher layer, it will be encoded in latin-1 bytes
        try:
            raw_input_bytes = plaintext.encode('utf-8')
        except UnicodeEncodeError:
            raw_input_bytes = plaintext.encode('latin-1')
        
        # 3. Initialize AES in CBC mode (generates a random, secure IV)
        cipher = AES.new(hashed_key, AES.MODE_CBC)
        
        # 4. Pad the text to match 16-byte block sizes and encrypt
        padded_data = pad(raw_input_bytes, AES.block_size)
        raw_ciphertext = cipher.encrypt(padded_data)
        
        # 5. Combine the IV and Ciphertext together so decrypt can read it later
        combined_data = cipher.iv + raw_ciphertext
        
        # 6. Return as a safe, clean Base64 string for your GUI textbox / loop transport
        return base64.b64encode(combined_data).decode('utf-8')
    except Exception as e:
        return f"Error: Encryption failed ({str(e)})"

def decrypt(ciphertext_base64, key):
    try:
        # 1. Force the key to match the exact same 32-byte hash layout
        hashed_key = hashlib.sha256(key.encode('utf-8')).digest()
        
        # 2. Handle Base64 decoding safely
        # If a previous cipher layer stripped the Base64, convert using latin-1
        try:
            combined_data = base64.b64decode(ciphertext_base64.encode('utf-8'))
        except Exception:
            # Fallback if the pipeline data is already raw binary transported via string
            combined_data = ciphertext_base64.encode('latin-1')
        
        # 3. Extract the original 16-byte IV from the front of the data array
        if len(combined_data) < 16:
            return "Error: Ciphertext data stream too short to extract AES IV block."
            
        iv = combined_data[:16]
        raw_ciphertext = combined_data[16:]
        
        # 4. Re-create the cipher engine instance using the extracted IV
        cipher = AES.new(hashed_key, AES.MODE_CBC, iv)
        
        # 5. Decrypt and strip the block alignment padding safely
        decrypted_padded = cipher.decrypt(raw_ciphertext)
        plain_bytes = unpad(decrypted_padded, AES.block_size)
        
        # 6. THE PIPELINE FIX: Safely determine if this is intermediate binary data or final text
        try:
            # If this is the final layer of your sequence loop, it returns clean text to display
            return plain_bytes.decode('utf-8')
        except UnicodeDecodeError:
            # If there are MORE ciphers left to process in the chain loop, pass it as a safe 
            # string wrapper. This prevents Python from crashing on raw encrypted bytes.
            return plain_bytes.decode('latin-1')
            
    except Exception as e:
        # Returning "Error:" text structure trips your GUI shield to handle layout errors gracefully
        return f"Error: Decryption failed ({str(e)})"