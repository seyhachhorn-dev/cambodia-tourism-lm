import os
from tokenizers import ByteLevelBPETokenizer

# 1. Gather all cleaned text files
files = []
for lang in ["en", "km"]:
    clean_dir = f"data/cleaned/{lang}"
    for filename in os.listdir(clean_dir):
        if filename.endswith(".txt"):
            files.append(os.path.join(clean_dir, filename))

print("Found files:", files)

# 2. Initialize the tokenizer
tokenizer = ByteLevelBPETokenizer()

# 3. Train the tokenizer on our specific dataset
print("\nTraining Byte-Level BPE tokenizer...")
tokenizer.train(
    files=files,
    vocab_size=16000,
    min_frequency=2,
    special_tokens=[
        "<|endoftext|>", # Marks the beginning/end of a document
        "<|pad|>"        # Used to make sequences the same length during training
    ]
)

# 4. Save the vocabulary and merges to the tokenizer directory
os.makedirs("tokenizer", exist_ok=True)
tokenizer.save_model("tokenizer")
print("\nTokenizer successfully saved in the 'tokenizer/' directory.")

# 5. Test the tokenizer on English and Khmer
test_en = "Angkor Wat is located in Siem Reap."
test_km = "ប្រាសាទអង្គរវត្តស្ថិតនៅខេត្តសៀមរាប។"

encoded_en = tokenizer.encode(test_en)
encoded_km = tokenizer.encode(test_km)

print(f"\n--- English Test ---")
print(f"Text: {test_en}")
print(f"Number of tokens: {len(encoded_en.tokens)}")
print(f"Tokens: {encoded_en.tokens}")

print(f"\n--- Khmer Test ---")
print(f"Text: {test_km}")
print(f"Number of tokens: {len(encoded_km.tokens)}")
print(f"Tokens: {encoded_km.tokens}")