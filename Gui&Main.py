import subprocess
import sys
import os                    

def install_dependencies():
    """Checks and installs libraries ONLY if they are actually missing."""
    dependencies = {
        "customtkinter": "customtkinter",
        "numpy": "numpy",
        "PIL": "Pillow",         
        "cryptography": "cryptography",
        "Crypto": "pycryptodome"
    }
    
    for import_name, pip_name in dependencies.items():
        try:
            __import__(import_name)
        except ImportError:
            print(f"[*] Missing library: {pip_name}. Installing now...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", pip_name])

# Execute installer before anything else  
install_dependencies()

# --- Standard Imports ---
import customtkinter as ctk
import importlib
import numpy as np 
import PIL.Image             
from PIL import ImageEnhance 
def global_decrypt_shield(ciphertext, key, decrypt_function):
    """
    Centralized shield that runs the cipher's decryption and intercepts
    any invalid keys or corrupted output before it can hit the GUI screen.
    """
    try:
        # Destroy invisible Tkinter formatting bytes right here
        if isinstance(ciphertext, str):
            ciphertext = ciphertext.strip()
        if isinstance(key, str):
            key = key.strip()

        # 1. Run the underlying module's decryption
        raw_output = decrypt_function(ciphertext, key)
        
        # If it's an internal error statement, pass it out immediately
        if "Error:" in str(raw_output) or "3DES Error:" in str(raw_output):
            return "Error: Decryption failed (Corrupted ciphertext layout)."
            
        # 2. Aggressively strip raw binary padding blocks 
        if isinstance(raw_output, str):
            clean_output = raw_output.rstrip('\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f\x10')
        else:
            clean_output = raw_output
            
        # 3. SCAN FOR TRUE GIBBERISH (Invalid Key Signals)
        if isinstance(clean_output, str):
            control_chars = [ord(c) for c in clean_output if ord(c) < 32 and c not in "\n\r\t"]
            if len(clean_output) > 0 and (len(control_chars) / len(clean_output)) > 0.15:
                return "Error: Invalid Key! Decryption failed."
            
        return clean_output
        
    except Exception as e:
        return f"Error: Decryption broken ({str(e)})."

# =====================================================================
# CIPHER MAP CONFIGURATION
# =====================================================================
CIPHER_MAP = {
    '0': 'Caesar', '1': 'Vigenere', '2': 'RailFence', '3': 'Atbash',
    '4': 'Columnar', '5': 'Rot13', '6': 'Xor', '7': 'Hill',
    '8': 'SimpleRev', '9': 'Base64', 'A': 'AES256', 'B': 'Blowfish',
    'C': 'ChaCha20', 'D': 'DES3', "E": "Elgamal", 'F': 'Fernet',
    "G": "Gost", "H": "Hebern", "I": "IDEA", "J": "Jumble",
    'K': 'Khufu', "L": "Lorenz", "M": "Multi2", "N": "Nihil",
    "O": "Orx", "P": "Present", "Q": "Quagmire", "R": "RC4",
    'S': 'Salsa20', "T": "Twofish", "U": "Ublock", "V": "Vest",
    "W": "Wake", "X": "XTEA", "Y": "Yuva", "Z": "ZuChongzhi",
    '#': 'LSB', "@": "Acrostic", "$": "GhostText", "%": "Baconian", "*": "InterlvdSpaces",
    "!": "Punctuation", "&": "WordCount", "~": "OpenLetter", "+": "VowelConsonant",
}

class CipherStudio(ctk.CTk):
    def __init__(self):
        super().__init__() # This MUST be first

        self.title("CYFR Studio")
        self.geometry("700x785")

        # --- BACKGROUND SECTION ---
        try:
            # Open the image (renamed to bg.jpg for simplicity)
            raw_bg = PIL.Image.open("bg.jpg")
            
            # Darken it so we can see the text
            raw_bg = ImageEnhance.Brightness(raw_bg).enhance(0.5) 

            self.bg_image = ctk.CTkImage(
                light_image=raw_bg,
                dark_image=raw_bg,
                size=(2000, 900)
            )

            # Create the label using 'self' because it belongs to this window
            self.bg_label = ctk.CTkLabel(self, image=self.bg_image, text="")
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except Exception as e:
            print(f"Background Error: {e}")

        # --- EVERYTHING ELSE BELOW ---
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")

        # --- THE LOGO SECTION ---
        ascii_logo = """
 ██████╗██╗   ██╗███████╗██████╗ 
██╔════╝╚██╗ ██╔╝██╔════╝██╔══██╗
██║      ╚████╔╝ █████╗  ██████╔╝
██║       ╚██╔╝  ██╔══╝  ██╔══██╗
╚██████╗   ██║   ██║     ██║  ██║
 ╚═════╝   ╚═╝   ╚═╝     ╚═╝  ╚═╝
"""
        self.logo_label = ctk.CTkLabel(
            self, 
            text=ascii_logo, 
            font=("Consolas", 10, "bold"), 
            text_color="#FF0000",
            justify="center"
        )
        # We use pack(side="top") to keep it at the summit of the UI
        self.logo_label.pack(pady=(10, 3), padx=20)
        # -------------------------

        ctk.set_appearance_mode("system")

        # --- UI ELEMENTS ---
        self.label = ctk.CTkLabel(self, text="Encryption System by NotQuite_77",text_color="#FF3131",font=("Consolas", 35, "italic","bold"))
        self.label.pack(pady=10)

        # --- THE MICRO CIPHER INDEX ---
        index_frame = ctk.CTkFrame(self, fg_color="transparent") # Transparent looks smaller
        index_frame.pack(pady=2, padx=20) 

        # Sub-container for the actual grid
        grid_container = ctk.CTkFrame(index_frame, fg_color="transparent")
        grid_container.pack()

        ciphers = list(CIPHER_MAP.items())
        
        # 6 columns makes the whole block very short (only 2-3 rows high)
        cols = 9 
        for i, (key_label, name) in enumerate(ciphers):
            row = i // cols
            col = i % cols
            
            slot_label = ctk.CTkLabel(
                grid_container, 
                text=f"[{key_label}]{name}", 
                font=("Consolas", 9, 'bold'), 
                text_color="#FFFFFF",
                anchor="w"
            )
            slot_label.grid(row=row, column=col, padx=4, pady=0, sticky="w")

        # Message Input
        self.msg_label = ctk.CTkLabel(self, text="Enter Message:")
        self.msg_label.pack()
        self.msg_input = ctk.CTkTextbox(self, height=90, width=500)
        self.msg_input.pack(pady=10)

        # Sequence Input
        self.seq_input = ctk.CTkEntry(self, placeholder_text="Sequence (e.g. 0279)", width=500)
        self.seq_input.pack(pady=10)

        # Key Input
        self.key_input = ctk.CTkEntry(self, placeholder_text="Master Key", show="*", width=500)
        self.key_input.pack(pady=10)

        # Mode Selection
        self.mode_var = ctk.StringVar(value="Encrypt")
        self.seg_button = ctk.CTkSegmentedButton(self, values=["Encrypt", "Decrypt"], variable=self.mode_var, selected_hover_color="darkblue")
        self.seg_button.pack(pady=10)

        # Action Button
        self.run_btn = ctk.CTkButton(self, text="EXECUTE", command=self.process, fg_color="red", hover_color="darkred")
        self.run_btn.pack(pady=5)

        # Result Output
        self.res_label = ctk.CTkLabel(self, text="Result:")
        self.res_label.pack()
        self.res_output = ctk.CTkTextbox(self, height=90, width=500)
        self.res_output.pack(pady=10)

# --- CLIPBOARD SHORTCUT FIXES ---
        # Force the text widgets to handle standard Windows shortcuts
        self.msg_input.bind("<Control-c>", lambda e: self.msg_input.event_generate("<<Copy>>"))
        self.msg_input.bind("<Control-v>", lambda e: self.msg_input.event_generate("<<Paste>>"))
        self.msg_input.bind("<Control-a>", lambda e: self.msg_input.focus_get().tag_add("sel", "1.0", "end"))

        self.res_output.bind("<Control-c>", lambda e: self.res_output.event_generate("<<Copy>>"))
        self.res_output.bind("<Control-v>", lambda e: self.res_output.event_generate("<<Paste>>"))
        self.res_output.bind("<Control-a>", lambda e: self.res_output.focus_get().tag_add("sel", "1.0", "end"))

    # =====================================================================
    # UNIFIED EXECUTION PIPELINE
    # =====================================================================
    def process(self):
        # 1. Clear output box and ensure state allows writing
        self.res_output.configure(state="normal")
        self.res_output.delete("1.0", "end")
        
        # 2. BULLETPROOF EXTRACTION: Check widget types dynamically
        try:
            if hasattr(self.msg_input, "_textbox"):  
                current_data = self.msg_input.get("1.0", "end").strip()
            else:                                    
                current_data = self.msg_input.get().strip()
        except Exception:
            current_data = ""

        try:
            if hasattr(self.seq_input, "_textbox"):
                sequence = self.seq_input.get("1.0", "end").strip()
            else:
                sequence = self.seq_input.get().strip()
        except Exception:
            sequence = ""

        try:
            if hasattr(self.key_input, "_textbox"):
                key = self.key_input.get("1.0", "end").strip()
            else:
                key = self.key_input.get().strip()
        except Exception:
            key = ""

        try:
            mode_clean = str(self.mode_var.get()).strip().lower()
        except Exception:
            mode_clean = "encrypt"

        # Defensive Validation Guard
        if not current_data:
            self.res_output.insert("1.0", "Error: Input text box is empty.")
            return
            
        if not sequence:
            self.res_output.insert("1.0", "Error: No routing sequence provided.")
            return

        # 3. DYNAMIC PIPELINE ENGINE PROCESSING BLOCK
        try:
            # Check for lower case strings safely and auto-reverse decryption codes
            loop_sequence = sequence[::-1] if mode_clean == "decrypt" else sequence
            
            for symbol in loop_sequence:
                if symbol not in CIPHER_MAP:
                    current_data = f"Error: Unknown routing character '{symbol}'."
                    break
                    
                selected_cipher = CIPHER_MAP[symbol]
                
                try:
                    module_path = f"Ciphers.{selected_cipher}"
                    cipher_module = importlib.import_module(module_path)
                except ImportError:
                    current_data = f"Error: Missing required script file 'Ciphers/{selected_cipher}.py'."
                    break

                # Case-insensitive operation routing
                if mode_clean == "encrypt":
                    if hasattr(cipher_module, "encrypt"):
                        current_data = cipher_module.encrypt(current_data, key)
                    else:
                        current_data = f"Error: {selected_cipher} has no encrypt() layout."
                        break
                else:
                    if hasattr(cipher_module, "decrypt"):
                        # Process through our robust shield system
                        shield_result = global_decrypt_shield(current_data, key, cipher_module.decrypt)
                        
                        # Bypass shield if it wiped output, revealing internal debug data
                        if not shield_result or str(shield_result).strip() == "":
                            current_data = cipher_module.decrypt(current_data, key)
                        else:
                            current_data = shield_result
                    else:   
                        current_data = f"Error: {selected_cipher} has no decrypt() layout."
                        break

                # Intercept runtime mid-loop pipeline errors immediately
                if "Error:" in str(current_data):
                    break

        except Exception as loop_error:
            current_data = f"Error: Process execution collapsed unexpectedly ({str(loop_error)})."

        # 4. FINAL SAFE UI OUTPUT PUSH
        if isinstance(current_data, (tuple, list)):
            final_text = str(current_data[0]) 
        else:
            final_text = str(current_data)
            
        # Push the verified transformation back out to your display box
        self.res_output.insert("1.0", final_text)


if __name__ == "__main__":
    app = CipherStudio()  
    app.mainloop()
