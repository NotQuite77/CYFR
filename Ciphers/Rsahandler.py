from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes

def generate_keys():
    """Generates a new RSA-4096 pair and saves them to files."""
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=4096
    )
    # Save Private Key
    with open("private_key.pem", "wb") as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ))
    # Save Public Key
    public_key = private_key.public_key()
    with open("public_key.pem", "wb") as f:
        f.write(public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ))
    return "Keys generated as 'private_key.pem' and 'public_key.pem'"

def encrypt_master_key(master_key, public_key_path="public_key.pem"):
    """Encrypts the Master Key using a Public Key."""
    with open(public_key_path, "rb") as f:
        public_key = serialization.load_pem_public_key(f.read())
    
    encrypted = public_key.encrypt(
        master_key.encode(),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return encrypted.hex()

def decrypt_master_key(encrypted_hex, private_key_path="private_key.pem"):
    """Decrypts the Master Key using your Private Key."""
    with open(private_key_path, "rb") as f:
        private_key = serialization.load_pem_private_key(f.read(), password=None)
    
    decrypted = private_key.decrypt(
        bytes.fromhex(encrypted_hex),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return decrypted.decode()