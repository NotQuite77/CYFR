import hashlib
import base64

class VestCipherEngine:
    def __init__(self, key_str):
        # Derive a robust 256-bit seed using SHA-256
        seed = hashlib.sha256(str(key_str).encode()).digest()
        
        # Initialize internal state vectors
        self.accumulator = int.from_bytes(seed[:4], 'big') & 0xFFFFFFFF
        self.counter = int.from_bytes(seed[4:6], 'big') & 0xFFFF
        
        # S-Box constant mask generated directly from the key remainder
        self.mask_constant = int.from_bytes(seed[6:10], 'big') | 0x01010101

    def _clock_keystream_byte(self):
        # 1. Update the counter vector linearly
        self.counter = (self.counter + 1) & 0xFFFF
        
        # 2. Mutate the Accumulator register via a non-linear feedback loop
        # Shift and mix with counter and mask steps
        feedback = (self.accumulator >> 5) ^ (self.counter << 3)
        self.accumulator = ((self.accumulator << 7) | (self.accumulator >> 25)) & 0xFFFFFFFF
        self.accumulator ^= (feedback ^ self.mask_constant) & 0xFFFFFFFF
        
        # 3. Extract the active 8-bit keystream layer from the center of the accumulator
        keystream_byte = (self.accumulator >> 12) & 0xFF
        return keystream_byte

    def crypt_stream(self, data_bytes):
        result = bytearray()
        for byte in data_bytes:
            # Generate the current bit-mask step
            k_byte = self._clock_keystream_byte()
            
            # XOR the data track
            cipher_byte = byte ^ k_byte
            result.append(cipher_byte)
            
            # Feed the cipher output back into the Accumulator to continuously scramble the mesh
            self.accumulator = (self.accumulator + cipher_byte) & 0xFFFFFFFF
            
        return bytes(result)

def encrypt(text, key):
    try:
        if not text: return ""
        engine = VestCipherEngine(key)
        data = text.encode('utf-8')
        
        # Process stream encryption
        encrypted_bytes = engine.crypt_stream(data)
        return base64.b64encode(encrypted_bytes).decode('utf-8')
    except Exception as e:
        return f"VEST Error: {str(e)}"

def decrypt(text, key):
    try:
        if not text: return ""
        data = base64.b64decode(text.encode('utf-8'))
        
        # Stream ciphers require rebuilding the engine state from baseline
        # Because the ciphertext bytes are fed back into the accumulator step-by-step,
        # we must decode using a modified feedback loop to match the state mutation exactly.
        engine = VestCipherEngine(key)
        
        result = bytearray()
        for byte in data:
            k_byte = engine._clock_keystream_byte()
            plain_byte = byte ^ k_byte
            result.append(plain_byte)
            
            # Key step: Feed the *received* cipher byte back into the accumulator
            engine.accumulator = (engine.accumulator + byte) & 0xFFFFFFFF
            
        return result.decode('utf-8')
    except Exception as e:
        return f"VEST Decrypt Error: {str(e)}"