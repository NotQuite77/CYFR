# CYFR Studio

A modular multi-layer encryption framework that allows users to create custom encryption pipelines by chaining multiple cipher algorithms together through a routing sequence.

Instead of relying on a single encryption method, CYFR Studio can apply multiple classical, modern, and experimental ciphers sequentially, creating highly customizable encryption paths.

---

## Features

* Multi-layer encryption pipelines
* Custom cipher routing sequences
* Dynamic cipher loading architecture
* GUI built with CustomTkinter
* Automatic encryption/decryption sequence reversal
* Centralized decryption protection system
* Error detection and corruption handling
* Steganography cipher support
* Classical and modern cipher integration
* Extensible plugin-based design

---

## How It Works

Users provide:

1. A message
2. A master key
3. A routing sequence

### Example

**Sequence**

```text
0279
```

**Encryption Flow**

```text
Message
  ↓
Caesar
  ↓
RailFence
  ↓
Hill
  ↓
Base64
  ↓
Ciphertext
```

For decryption, the sequence is automatically reversed:

```text
Ciphertext
  ↓
Base64
  ↓
Hill
  ↓
RailFence
  ↓
Caesar
  ↓
Original Message
```

---

## Supported Cipher Categories

### Classical Ciphers

* Caesar
* Vigenere
* RailFence
* Atbash
* Columnar
* Rot13
* Baconian
* Quagmire
* Nihil
* Hebern

### Modern Ciphers

* AES-256
* Blowfish
* ChaCha20
* Salsa20
* Twofish
* XTEA
* RC4
* Fernet
* Triple DES

### Experimental Ciphers

* Khufu
* Multi2
* Lorenz
* Wake
* Yuva
* Vest
* ZuChongzhi

### Steganographic Modules

* LSB
* Acrostic
* GhostText
* OpenLetter
* WordCount
* Punctuation
* VowelConsonant

---

## Architecture

CYFR Studio uses a modular plugin system.

Each cipher exists as an independent Python module:

```text
Ciphers/
├── Caesar.py
├── AES256.py
├── ChaCha20.py
├── Blowfish.py
└── ...
```

Every module follows a common interface:

```python
def encrypt(data, key):
    pass

def decrypt(data, key):
    pass
```

Modules are loaded dynamically at runtime using Python's import system.

---

## Security Layer

CYFR Studio includes a centralized decryption shield that:

* Detects corrupted ciphertext
* Removes invalid padding artifacts
* Identifies likely incorrect keys
* Prevents malformed output from reaching the GUI
* Handles module failures gracefully

---

## Installation

Install dependencies:

```bash
pip install customtkinter numpy pillow cryptography pycryptodome
```

Run the application:

```bash
python main.py
```

---

## Cipher Routing Index

| Symbol | Cipher         |
| ------ | -------------- |
| 0      | Caesar         |
| 1      | Vigenere       |
| 2      | RailFence      |
| 3      | Atbash         |
| 4      | Columnar       |
| 5      | Rot13          |
| 6      | XOR            |
| 7      | Hill           |
| 8      | SimpleRev      |
| 9      | Base64         |
| A      | AES256         |
| B      | Blowfish       |
| C      | ChaCha20       |
| D      | DES3           |
| E      | ElGamal        |
| F      | Fernet         |
| G      | Gost           |
| H      | Hebern         |
| I      | IDEA           |
| J      | Jumble         |
| K      | Khufu          |
| L      | Lorenz         |
| M      | Multi2         |
| N      | Nihil          |
| O      | Orx            |
| P      | Present        |
| Q      | Quagmire       |
| R      | RC4            |
| S      | Salsa20        |
| T      | Twofish        |
| U      | Ublock         |
| V      | Vest           |
| W      | Wake           |
| X      | XTEA           |
| Y      | Yuva           |
| Z      | ZuChongzhi     |
| #      | LSB            |
| @      | Acrostic       |
| $      | GhostText      |
| %      | Baconian       |
| *      | InterlvdSpaces |
| !      | Punctuation    |
| &      | WordCount      |
| ~      | OpenLetter     |
| +      | VowelConsonant |

---

## Disclaimer

CYFR Studio is an educational and experimental cryptography framework.

While it contains modern cryptographic algorithms, the overall security of a custom encryption chain depends on implementation quality, key management, algorithm configuration, and cryptographic review.

This project should **not** be considered a replacement for professionally audited cryptographic systems used in production environments.

---

## Author

**NotQuite_77**

**CYFR Studio**
Custom Encryption Routing Framework

(I vibecoded the whole thing by the way)
