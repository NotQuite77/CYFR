import math

def encrypt(text, key):
    # Ensure key is a string
    key = str(key)
    n_cols = len(key)
    
    # Padding: Add spaces so text fits perfectly into the grid (rectangle)
    n_rows = math.ceil(len(text) / n_cols)
    padding_needed = (n_rows * n_cols) - len(text)
    text += " " * padding_needed
    
    # Sort key to get the column order
    key_order = sorted(range(len(key)), key=lambda k: key[k])
    
    # Create the grid
    grid = [text[i:i + n_cols] for i in range(0, len(text), n_cols)]
    
    # Read columns based on key order
    cipher = ""
    for col_idx in key_order:
        for row in grid:
            cipher += row[col_idx]
            
    return cipher

def decrypt(text, key):
    key = str(key)
    n_cols = len(key)
    
    # Safety: If text length isn't a multiple of key, padding was lost
    if len(text) % n_cols != 0:
        # Pad with spaces to prevent 'index out of range'
        text += " " * (n_cols - (len(text) % n_cols))
        
    n_rows = len(text) // n_cols
    key_order = sorted(range(len(key)), key=lambda k: key[k])
    
    # Create empty grid
    grid = [['' for _ in range(n_cols)] for _ in range(n_rows)]
    
    # Fill the grid column by column based on the sorted key order
    text_ptr = 0
    for col_idx in key_order:
        for row_idx in range(n_rows):
            if text_ptr < len(text):
                grid[row_idx][col_idx] = text[text_ptr]
                text_ptr += 1
                
    # Read rows to get original text
    result = "".join(["".join(row) for row in grid])
    return result.strip()