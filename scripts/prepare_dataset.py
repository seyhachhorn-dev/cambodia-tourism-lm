import os
import torch
from transformers import PreTrainedTokenizerFast
from tokenizers import ByteLevelBPETokenizer

print("Loading tokenizer...")
# Load the base BPE tokenizer we created in Step 8
base_tokenizer = ByteLevelBPETokenizer(
    "tokenizer/vocab.json",
    "tokenizer/merges.txt"
)

# Wrap it cleanly into a Hugging Face Fast Tokenizer
tokenizer = PreTrainedTokenizerFast(
    tokenizer_object=base_tokenizer._tokenizer
)

# Define the special tokens
tokenizer.add_special_tokens({
    "bos_token": "<|endoftext|>",
    "eos_token": "<|endoftext|>",
    "pad_token": "<|pad|>"
})

print("Reading cleaned text files...")
all_text = ""
for lang in ["en", "km"]:
    clean_dir = f"data/cleaned/{lang}"
    if not os.path.exists(clean_dir): 
        continue
    for filename in os.listdir(clean_dir):
        if filename.endswith(".txt"):
            with open(os.path.join(clean_dir, filename), "r", encoding="utf-8") as f:
                # Insert the special end-of-text token to tell the model when an article ends
                all_text += f.read() + "\n<|endoftext|>\n"

print("Tokenizing entire corpus...")
tokens = tokenizer.encode(all_text)
print(f"Total tokens in dataset: {len(tokens):,}")

context_length = 512
print(f"Packing into blocks of {context_length} tokens...")

input_ids = []
labels = []

# Slide through the tokens and chop them into exact 512-token blocks
for i in range(0, len(tokens) - context_length, context_length):
    block = tokens[i : i + context_length]
    input_ids.append(block)
    labels.append(block)

# Split the dataset: 90% for training, 10% for validation
split_idx = int(len(input_ids) * 0.9)
train_inputs = torch.tensor(input_ids[:split_idx])
train_labels = torch.tensor(labels[:split_idx])

val_inputs = torch.tensor(input_ids[split_idx:])
val_labels = torch.tensor(labels[split_idx:])

os.makedirs("data/train", exist_ok=True)
os.makedirs("data/validation", exist_ok=True)

# Save the packed mathematical tensors directly to the hard drive
torch.save({"input_ids": train_inputs, "labels": train_labels}, "data/train/dataset.pt")
torch.save({"input_ids": val_inputs, "labels": val_labels}, "data/validation/dataset.pt")

print(f"\n--- Dataset Prepared ---")
print(f"Training blocks: {len(train_inputs)}")
print(f"Validation blocks: {len(val_inputs)}")
print("Saved to data/train/ and data/validation/")