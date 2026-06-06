import hashlib
import base64
import struct

# Twofish fixed permutation tables (Q0 and Q1) used to build key-dependent S-boxes
Q0 = [
    [0xA9, 0x67, 0xB3, 0xE8, 0x04, 0xFD, 0xA3, 0x76, 0x9A, 0x92, 0x80, 0x78, 0xE4, 0xDD, 0xD1, 0x38],
    [0x0D, 0xC6, 0x35, 0x98, 0x18, 0xF7, 0xEC, 0x6C, 0x43, 0x75, 0x37, 0x26, 0xFA, 0x13, 0x94, 0x48],
    [0xF2, 0xD0, 0x8B, 0x30, 0x84, 0xAF, 0x32, 0x61, 0x0E, 0x1F, 0x5E, 0x21, 0x5C, 0x1A, 0xA2, 0x02],
    [0x81, 0x4E, 0x60, 0xCE, 0xA1, 0x8A, 0x12, 0x10, 0x7D, 0x58, 0x1A, 0x7C, 0x57, 0x3D, 0x47, 0xDF]
]

# RS matrix coefficients for key schedule computation
RS = [
    [0x01, 0xA4, 0x55, 0x87, 0x5A, 0x58, 0xDB, 0x9E],
    [0xA4, 0x56, 0x82, 0xF3, 0X1E, 0XC6, 0X68, 0XE5],
    [0x02, 0xA1, 0xFC, 0xC1, 0x47, 0xAE, 0x3D, 0x19],
    [0xA4, 0x55, 0x87, 0x5A, 0x58, 0xDB, 0x9E, 0x03]
]

# MDS matrix linear coefficients
MDS = [
    [0x01, 0xEF, 0x5B, 0x5B],
    [0x5B, 0xEF, 0xEF, 0x01],
    [0xEF, 0x5B, 0x01, 0xEF],
    [0xEF, 0x01, 0xEF, 0x5B]
]

def gf_mul(a, b, poly=0x169):
    # Galois Field multiplication over GF(2^8)
    p = 0
    for _ in range(8):
        if b & 1:
            p ^= a
        hi = a & 0x80
        a = (a << 1) & 0xFF
        if hi:
            a ^= (poly & 0xFF)
        b >>= 1
    return p

def mds_mix(x0, x1, x2, x3):
    # Vector matrix multiplication using the MDS layout
    b0 = gf_mul(x0, MDS[0][0]) ^ gf_mul(x1, MDS[0][1]) ^ gf_mul(x2, MDS[0][2]) ^ gf_mul(x3, MDS[0][3])
    b1 = gf_mul(x0, MDS[1][0]) ^ gf_mul(x1, MDS[1][1]) ^ gf_mul(x2, MDS[1][2]) ^ gf_mul(x3, MDS[1][3])
    b2 = gf_mul(x0, MDS[2][0]) ^ gf_mul(x1, MDS[2][1]) ^ gf_mul(x2, MDS[2][2]) ^ gf_mul(x3, MDS[2][3])
    b3 = gf_mul(x0, MDS[3][0]) ^ gf_mul(x1, MDS[3][1]) ^ gf_mul(x2, MDS[3][2]) ^ gf_mul(x3, MDS[3][3])
    return b0 | (b1 << 8) | (b2 << 16) | (b3 << 24)

def h_func(X, L):
    # Core internal H-function mapping byte mutations deterministically
    x0 = X & 0xFF
    x1 = (X >> 8) & 0xFF
    x2 = (X >> 16) & 0xFF
    x3 = (X >> 24) & 0xFF
    
    # Mix with the key-dependent vectors L derived in key schedule
    x0 ^= L[0]
    x1 ^= L[1]
    x2 ^= L[2]
    x3 ^= L[3]
    
    # Pass through fixed algebraic substitution approximations
    x0 = Q0[0][x0 >> 4] ^ Q0[1][x0 & 0xF]
    x1 = Q0[2][x1 >> 4] ^ Q0[3][x1 & 0xF]
    x2 = Q0[0][x2 >> 4] ^ Q0[2][x2 & 0xF]
    x3 = Q0[1][x3 >> 4] ^ Q0[3][x3 & 0xF]
    
    return mds_mix(x0, x1, x2, x3)

def generate_key_schedule(key_str):
    # Force master password down to uniform 256-bit hash boundary
    h = hashlib.sha256(str(key_str).encode()).digest()
    
    # Twofish splits a 256-bit key into vector groups
    L = [list(h[i:i+4]) for i in range(0, 32, 4)]
    
    subkeys = []
    # Generate 40 round keys using Pseudo-Hadamard Transform pairs
    for i in range(0, 40, 2):
        A = h_func(i * 0x02020202, L[0])
        B = h_func((i + 1) * 0x02020202, L[1])
        B = ((B << 8) | (B >> 24)) & 0xFFFFFFFF
        
        # PHT step
        subkey_A = (A + B) & 0xFFFFFFFF
        subkey_B = (A + 2 * B) & 0xFFFFFFFF
        subkey_B = ((subkey_B << 9) | (subkey_B >> 23)) & 0xFFFFFFFF
        
        subkeys.append(subkey_A)
        subkeys.append(subkey_B)
        
    return subkeys, L[2] # Return derived schedule keys and S-box vector baseline

def twofish_block(block, subkeys, S_box_vector, encrypt_mode=True):
    words = list(struct.unpack("<IIII", block))
    
    if encrypt_mode:
        # Input Whitening step
        words[0] ^= subkeys[0]
        words[1] ^= subkeys[1]
        words[2] ^= subkeys[2]
        words[3] ^= subkeys[3]
        
        # 16 Feistel Rounds
        for r in range(16):
            t0 = h_func(words[0], S_box_vector)
            t1 = h_func(((words[1] << 8) | (words[1] >> 24)) & 0xFFFFFFFF, S_box_vector)
            
            # PHT mixing
            f0 = (t0 + t1) & 0xFFFFFFFF
            f1 = (t0 + 2 * t1) & 0xFFFFFFFF
            
            # Key mixing layer incorporation
            k_offset = 8 + r * 2
            f0 = (f0 + subkeys[k_offset]) & 0xFFFFFFFF
            f1 = (f1 + subkeys[k_offset + 1]) & 0xFFFFFFFF
            
            # XOR into opposite half and rotate
            words[2] ^= f0
            words[2] = ((words[2] >> 1) | (words[2] << 31)) & 0xFFFFFFFF
            words[3] = ((words[3] << 1) | (words[3] >> 31)) & 0xFFFFFFFF
            words[3] ^= f1
            
            if r < 15:
                words[0], words[1], words[2], words[3] = words[2], words[3], words[0], words[1]
                
        # Output Whitening step
        words[2] ^= subkeys[4]
        words[3] ^= subkeys[5]
        words[0] ^= subkeys[6]
        words[1] ^= subkeys[7]
        return struct.pack("<IIII", words[2], words[3], words[0], words[1])
    else:
        # Decryption unrolls whitening backwards
        words[0] ^= subkeys[4]
        words[1] ^= subkeys[5]
        words[2] ^= subkeys[6]
        words[3] ^= subkeys[7]
        
        for r in range(15, -1, -1):
            t0 = h_func(words[2], S_box_vector)
            t1 = h_func(((words[3] << 8) | (words[3] >> 24)) & 0xFFFFFFFF, S_box_vector)
            
            f0 = (t0 + t1) & 0xFFFFFFFF
            f1 = (t0 + 2 * t1) & 0xFFFFFFFF
            
            k_offset = 8 + r * 2
            f0 = (f0 + subkeys[k_offset]) & 0xFFFFFFFF
            f1 = (f1 + subkeys[k_offset + 1]) & 0xFFFFFFFF
            
            # Reverse rotations and XOR
            words[0] = ((words[0] << 1) | (words[0] >> 31)) & 0xFFFFFFFF
            words[0] ^= f0
            words[1] ^= f1
            words[1] = ((words[1] >> 1) | (words[1] << 31)) & 0xFFFFFFFF
            
            if r > 0:
                words[0], words[1], words[2], words[3] = words[2], words[3], words[0], words[1]
                
        words[2] ^= subkeys[0]
        words[3] ^= subkeys[1]
        words[0] ^= subkeys[2]
        words[1] ^= subkeys[3]
        return struct.pack("<IIII", words[0], words[1], words[2], words[3])

def encrypt(text, key):
    try:
        if not text: return ""
        subkeys, s_vector = generate_key_schedule(key)
        
        # 16-byte block alignment padding
        pad_len = 16 - (len(text) % 16)
        padded_text = text + (chr(pad_len) * pad_len)
        data = padded_text.encode('utf-8')
        
        result = b""
        for i in range(0, len(data), 16):
            result += twofish_block(data[i:i+16], subkeys, s_vector, encrypt_mode=True)
        return base64.b64encode(result).decode('utf-8')
    except Exception as e:
        return f"Twofish Error: {str(e)}"

def decrypt(text, key):
    try:
        if not text: return ""
        subkeys, s_vector = generate_key_schedule(key)
        data = base64.b64decode(text.encode('utf-8'))
        
        result = b""
        for i in range(0, len(data), 16):
            result += twofish_block(data[i:i+16], subkeys, s_vector, encrypt_mode=False)
            
        pad_len = result[-1]
        if 0 < pad_len <= 16:
            padding_bytes = result[-pad_len:]
            if all(b == pad_len for b in padding_bytes):
                return result[:-pad_len].decode('utf-8')
        return result.decode('utf-8', errors='replace')
    except Exception as e:
        return f"Twofish Decrypt Error: {str(e)}"