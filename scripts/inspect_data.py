import os

def inspect_dataset(lang):
    clean_dir = f"data/cleaned/{lang}"
    total_chars = 0
    total_lines = 0
    files_count = 0
    sample_text = ""
    
    if not os.path.exists(clean_dir):
        print(f"Directory {clean_dir} not found.")
        return
        
    for filename in os.listdir(clean_dir):
        if not filename.endswith(".txt"):
            continue
        
        filepath = os.path.join(clean_dir, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            text = f.read()
            
        files_count += 1
        total_chars += len(text)
        total_lines += text.count('\n') + 1
        
        # Grab a small sample from the first file we process
        if not sample_text and len(text) > 0:
            sample_text = text[:250] + "..."
            
    print(f"--- Language: {lang.upper()} ---")
    print(f"Documents: {files_count}")
    print(f"Total Lines (Paragraphs): {total_lines}")
    print(f"Total Characters: {total_chars}")
    print(f"Sample Text:\n{sample_text}\n")

print("Inspecting Cleaned Dataset...\n")
inspect_dataset("en")
inspect_dataset("km")