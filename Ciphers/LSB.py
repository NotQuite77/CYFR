from PIL import Image
import os
from pathlib import Path

def encrypt(text, key=None):
    # This finds the directory where Gui.py is (one level up from this file)
    base_path = Path(__file__).resolve().parent.parent
    input_path = base_path / "input.png"
    output_path = base_path / "secret.png"

    try:
        # Check if file exists using the absolute path
        if not input_path.exists():
            return f"Error: input.png not found at {input_path}"

        # Open image and ensure it's in RGB mode (required for bit manipulation)
        img = Image.open(input_path).convert("RGB")
        binary_msg = ''.join(format(ord(i), '08b') for i in text) + '1111111111111110'
        
        pixels = img.load()
        width, height = img.size
        
        # Check if image is big enough
        if len(binary_msg) > width * height:
            return "Error: Image too small for this much text!"

        idx = 0
        for y in range(height):
            for x in range(width):
                if idx < len(binary_msg):
                    r, g, b = pixels[x, y]
                    r = (r & ~1) | int(binary_msg[idx])
                    pixels[x, y] = (r, g, b)
                    idx += 1
        
        # Force save to the base directory
        img.save(output_path, "PNG")
        return f"SUCCESS: Saved to {output_path.name}"

    except Exception as e:
        return f"Stegano Error: {str(e)}"

def decrypt(text_not_used, key=None):
    base_path = Path(__file__).resolve().parent.parent
    secret_path = base_path / "secret.png"

    try:
        if not secret_path.exists():
            return "Error: secret.png not found!"

        img = Image.open(secret_path).convert("RGB")
        pixels = img.load()
        width, height = img.size
        
        binary_msg = ""
        for y in range(height):
            for x in range(width):
                r, g, b = pixels[x, y]
                binary_msg += str(r & 1)
        
        # Look for the 16-bit EOF marker
        marker = '1111111111111110'
        end_idx = binary_msg.find(marker)
        if end_idx == -1:
            return "Error: No hidden message found in image."

        binary_msg = binary_msg[:end_idx]
        
        # Convert bits back to characters
        all_bytes = [binary_msg[i:i+8] for i in range(0, len(binary_msg), 8)]
        decoded_text = "".join([chr(int(b, 2)) for b in all_bytes])
            
        return decoded_text
    except Exception as e:
        return f"Stegano Decrypt Error: {e}"