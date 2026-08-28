from transformers import LlamaConfig, LlamaForCausalLM

# Define the blueprint for our custom LLM
config = LlamaConfig(
    vocab_size=16000,           # Must match our tokenizer's target size
    hidden_size=384,            # The "width" of the model's brain
    intermediate_size=1024,     # The size of the feed-forward layer
    num_hidden_layers=8,        # How many Transformer blocks to stack
    num_attention_heads=6,      # How many parallel attention processes
    max_position_embeddings=512,# Maximum context length (tokens it can read at once)
    pad_token_id=1,
    bos_token_id=0,
    eos_token_id=0,
    tie_word_embeddings=True    # Shares weights between input/output to save VRAM
)

# Initialize the model from the blueprint (RANDOM WEIGHTS)
model = LlamaForCausalLM(config)

# Calculate the exact size
total_params = sum(p.numel() for p in model.parameters())

print("--- Model Architecture Initialized ---")
print(f"Total Parameters: {total_params:,}")

# Save the configuration for training later
config.save_pretrained("configs")
print("Blueprint saved to configs/")