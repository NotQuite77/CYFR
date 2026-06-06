import hashlib
import base64

class LorenzMachine:
    def __init__(self, key_str):
        # Official Lorenz wheel sizes (totaling 501 pins)
        self.CHI_SIZES = [41, 31, 29, 26, 23]
        self.PSI_SIZES = [43, 47, 51, 53, 59]
        self.MOTOR_SIZES = [59, 37] # Clear text names: M1 and M2
        
        # Derive deterministic pin patterns from the key
        hash_seed = hashlib.sha256(str(key_str).encode()).digest()
        
        # Generate the pin distributions (1 = pin active/set, 0 = inactive)
        self.chi_pins = self._generate_pins(self.CHI_SIZES, hash_seed, 0)
        self.psi_pins = self._generate_pins(self.PSI_SIZES, hash_seed, 5)
        self.motor_pins = self._generate_pins(self.MOTOR_SIZES, hash_seed, 10)
        
        # Initialize wheel positions (starting indexes)
        self.chi_pos = [0] * 5
        self.psi_pos = [0] * 5
        self.motor_pos = [0] * 2

    def _generate_pins(self, sizes, seed, offset):
        pins = []
        for i, size in enumerate(sizes):
            # Mutate seed slightly for each wheel to ensure different pin behaviors
            wheel_seed = hashlib.sha256(seed + bytes([offset + i])).digest()
            wheel_pins = []
            for bit_idx in range(size):
                byte_pos = (bit_idx // 8) % len(wheel_seed)
                bit_pos = bit_idx % 8
                # Extract individual bits to use as pin settings
                wheel_pins.append((wheel_seed[byte_pos] >> bit_pos) & 1)
            pins.append(wheel_pins)
        return pins

    def clock_bit(self):
        # 1. Read current active values from wheels
        chi_val = 0
        for i in range(5):
            chi_val ^= self.chi_pins[i][self.chi_pos[i]]
            
        psi_val = 0
        for i in range(5):
            psi_val ^= self.psi_pins[i][self.psi_pos[i]]
            
        # The output keystream bit is the XOR summation of Chi and Psi values
        keystream_bit = chi_val ^ psi_val
        
        # 2. Advance the wheels based on mechanical motor logic
        # Chi wheels ALWAYS step forward
        for i in range(5):
            self.chi_pos[i] = (self.chi_pos[i] + 1) % self.CHI_SIZES[i]
            
        # Motor wheel 1 ALWAYS steps forward
        m1_pin = self.motor_pins[0][self.motor_pos[0]]
        self.motor_pos[0] = (self.motor_pos[0] + 1) % self.MOTOR_SIZES[0]
        
        # Motor wheel 2 steps ONLY if Motor wheel 1's pin was active
        if m1_pin == 1:
            m2_pin = self.motor_pins[1][self.motor_pos[1]]
            self.motor_pos[1] = (self.motor_pos[1] + 1) % self.MOTOR_SIZES[1]
            
            # If Motor wheel 2's pin is active, ALL Psi wheels step forward
            if m2_pin == 1:
                for i in range(5):
                    self.psi_pos[i] = (self.psi_pos[i] + 1) % self.PSI_SIZES[i]
                    
        return keystream_bit

    def clock_byte(self):
        # Collect 8 keystream bits to form a complete byte
        out_byte = 0
        for b in range(8):
            out_byte |= (self.clock_bit() << b)
        return out_byte

def encrypt(text, key):
    try:
        if not text: return ""
        machine = LorenzMachine(key)
        data = text.encode('utf-8')
        
        result = bytearray()
        for byte in data:
            # XOR the data stream with the virtual mechanical wheel output
            result.append(byte ^ machine.clock_byte())
            
        return base64.b64encode(result).decode('utf-8')
    except Exception as e:
        return f"Lorenz Error: {str(e)}"

def decrypt(text, key):
    try:
        if not text: return ""
        machine = LorenzMachine(key)
        data = base64.b64decode(text.encode('utf-8'))
        
        result = bytearray()
        for byte in data:
            # Stream ciphers reverse perfectly using identical XOR operations
            result.append(byte ^ machine.clock_byte())
            
        return result.decode('utf-8')
    except Exception as e:
        return f"Lorenz Decrypt Error: {str(e)}"