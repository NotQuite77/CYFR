import hashlib
import base64
import struct

def generate_round_keys(key_str):
    # Hash the master password down to create 8 unique 64-bit round keys
    h = hashlib.sha512(str(key_str).encode()).digest()
    round_keys = []
    for i in range(8):
        # Extract 8-byte chunks from the 64-byte hash stream
        chunk = h[i*8 : (i+1)*8]
        round_keys.append(list(chunk))
    return round_keys

def encrypt(text, key):
    try:
        if not text: return ""
        r_keys = generate_round_keys(key)
        
        # Standard 8-byte block alignment padding
        pad_len = 8 - (len(text) % 8)
        padded_text = text + (chr(pad_len) * pad_len)
        data = padded_text.encode('utf-8')
        
        result = b""
        for b_idx in range(0, len(data), 8):
            # Unpack block into 8 individual bytes
            state = list(data[b_idx:b_idx+8])
            
            # Execute 8 core rounds
            for r in range(8):
                rk = r_keys[r]
                
                # Step 1: Key Mixing (XOR)
                state = [state[i] ^ rk[i] for i in range(8)]
                
                # Step 2: Non-Linear Prime Multiplier Layer
                # Multiply by a prime constant derived from the key, modulo 257
                prime_factor = (rk[7] | 1) # Ensure it's odd
                state = [((b * prime_factor) + r) % 257 for b in state]
                # Keep values safely bound to 8 bits
                state = [b & 0xFF if b < 256 else 0 for b in state]
                
                # Step 3: Diffusion Shift Layer
                if r % 2 == 0:
                    # Even rounds: Invert all bits completely
                    state = [(~b) & 0xFF for b in state]
                else:
                    # Odd rounds: Circular shift left by 3 positions
                    state = state[3:] + state[:3]
                    
            result += bytes(state)
            
        return base64.b64encode(result).decode('utf-8')
    except Exception as e:
        return f"UBLOCK Error: {str(e)}"

def decrypt(text, key):
    try:
        if not text: return ""
        r_keys = generate_round_keys(key)
        data = base64.b64decode(text.encode('utf-8'))
        
        result = b""
        for b_idx in range(0, len(data), 8):
            state = list(data[b_idx:b_idx+8])
            
            # Run the 8 rounds in absolute mathematical reverse (7 down to 0)
            for r in range(7, -1, -1):
                rk = r_keys[r]
                
                # Undo Step 3: Reverse the Diffusion Layer
                if r % 2 == 0:
                    # Bitwise inversion is its own inverse!
                    state = [(~b) & 0xFF for b in state]
                else:
                    # Reverse circular shift: shift right by 3 positions
                    state = state[-3:] + state[:-3]
                    
                # Undo Step 2: Reverse Multiplicative Mixing via modular multiplicative inverse
                prime_factor = (rk[7] | 1)
                # Compute modular inverse for modulo 257
                inv_prime = pow(prime_factor, -1, 257)
                
                for i in range(8):
                    val = state[i]
                    # Subtract the round variable back out
                    val = (val - r) % 257
                    # Multiply by inverse to restore original byte state
                    orig_b = (val * inv_prime) % 257
                    state[i] = orig_b if orig_b < 256 else 0
                    
                # Undo Step 1: Key Mixing (XOR is its own inverse)
                state = [state[i] ^ rk[i] for i in range(8)]
                
            result += bytes(state)
            
        # Strip padding bytes safely out
        pad_len = result[-1]
        if 0 < pad_len <= 8:
            padding_bytes = result[-pad_len:]
            if all(b == pad_len for b in padding_bytes):
                return result[:-pad_len].decode('utf-8')
        return result.decode('utf-8', errors='replace')
    except Exception as e:
        return f"UBLOCK Decrypt Error: {str(e)}"