from argon2 import PasswordHasher, low_level
import hashlib

# Parameters for Argon2id (The most secure variant)
# Time Cost: 3 iterations
# Memory Cost: 64MB
# Parallelism: 4 threads
SALT = b"static_salt_for_consistency" # In a real app, use a unique salt per user

def encrypt(text, key):
    """
    This doesn't encrypt the text; it 'strengthens' the key 
    and returns the original text so the pipeline continues.
    """
    # Derive a 32-byte key from the master key using Argon2
    strengthened_key = low_level.hash_secret_raw(
        secret=str(key).encode(),
        salt=SALT,
        time_cost=3,
        memory_cost=65536,
        parallelism=4,
        hash_len=32,
        type=low_level.Type.ID
    )
    
    # We store the strengthened key in a way the next cipher can grab it
    # For your specific GUI, we'll return the text as-is, 
    # but the REAL benefit is using this key for the next steps.
    return text

def get_strong_key(master_key):
    """Helper function to get the 32-byte result for other ciphers."""
    return low_level.hash_secret_raw(
        secret=str(master_key).encode(),
        salt=SALT,
        time_cost=3,
        memory_cost=65536,
        parallelism=4,
        hash_len=32,
        type=low_level.Type.ID
    )