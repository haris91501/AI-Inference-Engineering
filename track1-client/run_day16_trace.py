import json
import torch
from transformers import AutoTokenizer, AutoModel

model_id = "gpt2"
print(f"Loading {model_id} tokenizer & model...")
tokenizer = AutoTokenizer.from_pretrained(model_id)
tokenizer.pad_token = tokenizer.eos_token
model = AutoModel.from_pretrained(model_id)

prompts = [
    "Inference is fast.",
    "Tokens matter for latency.",
    "Transformers process full sequence batches in parallel."
]

# 1. Unpadded tokenization (individual inspection)
print("\n--- UNPADDED INDIVIDUAL SHAPES ---")
unpadded_info = []
for p in prompts:
    enc = tokenizer(p, return_tensors="pt")
    shape_ids = list(enc["input_ids"].shape)
    print(f"Prompt: \"{p}\" | input_ids: {shape_ids} | tokens: {enc['input_ids'].tolist()[0]}")
    unpadded_info.append({"prompt": p, "shape": shape_ids, "ids": enc["input_ids"].tolist()[0]})

# 2. Padded batch tokenization
print("\n--- PADDED BATCH TENSORS ---")
batch_enc = tokenizer(prompts, padding=True, return_tensors="pt")
input_ids = batch_enc["input_ids"]
attention_mask = batch_enc["attention_mask"]

print(f"Batch input_ids shape:      {list(input_ids.shape)} | dtype: {input_ids.dtype}")
print(f"Batch attention_mask shape: {list(attention_mask.shape)} | dtype: {attention_mask.dtype}")
print("Attention Mask matrix:\n", attention_mask)

# 3. Embedding Lookup
# GPT-2 me embedding layer: model.wte (word token embeddings)
with torch.no_grad():
    token_embeddings = model.wte(input_ids)

print("\n--- EMBEDDING OUTPUT ---")
print(f"Embedding matrix weight shape: {list(model.wte.weight.shape)} (vocab_size, hidden_dim)")
print(f"Output embeddings shape:       {list(token_embeddings.shape)} [Batch, Seq_Len, Hidden_Dim]")
print(f"Output dtype:                  {token_embeddings.dtype}")

# 4. Save trace deliverable
trace_payload = {
    "model_id": model_id,
    "prompts": prompts,
    "padded_batch_shape": list(input_ids.shape),
    "attention_mask": attention_mask.tolist(),
    "embeddings_shape": list(token_embeddings.shape),
    "embeddings_dtype": str(token_embeddings.dtype)
}
with open("artifacts/day16-token-trace.json", "w") as f:
    json.dump(trace_payload, f, indent=2)

print("\nSuccessfully wrote artifacts/day16-token-trace.json")
