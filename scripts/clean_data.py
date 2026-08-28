import os
import re

# Ensure the clean directories exist
os.makedirs("data/cleaned/en", exist_ok=True)
os.makedirs("data/cleaned/km", exist_ok=True)

def clean_text(text):
    cleaned_lines = []
    
    for line in text.split('\n'):
        # Remove whitespace at the start and end of the line
        line = line.strip()
        
        # Skip completely empty lines
        if not line:
            continue
            
        # Skip Wikipedia section headers (e.g., "== Background ==")
        if line.startswith('==') and line.endswith('=='):
            continue
            
        # Keep lines that have enough text to form a meaningful sentence
        if len(line) > 15:
            # Replace multiple spaces with a single space
            line = re.sub(r'\s+', ' ', line)
            cleaned_lines.append(line)
            
    # Rejoin the surviving lines with a single newline
    return '\n'.join(cleaned_lines)

print("Starting data cleaning pipeline...")

for lang in ["en", "km"]:
    raw_dir = f"data/raw/{lang}"
    clean_dir = f"data/cleaned/{lang}"
    
    for filename in os.listdir(raw_dir):
        if not filename.endswith(".txt"):
            continue
            
        raw_path = os.path.join(raw_dir, filename)
        clean_path = os.path.join(clean_dir, filename)
        
        with open(raw_path, "r", encoding="utf-8") as f:
            raw_text = f.read()
            
        cleaned_text = clean_text(raw_text)
        
        with open(clean_path, "w", encoding="utf-8") as f:
            f.write(cleaned_text)
            
        print(f"Cleaned {filename} -> Reduced from {len(raw_text)} to {len(cleaned_text)} characters")

print("\nData cleaning complete! Cleaned texts are saved in data/cleaned/")