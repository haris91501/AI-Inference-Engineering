import torch

BATCH_SIZE = 2
SEQ_LEN = 4
HIDDEN_DIM = 128
VOCAB_SIZE = 32000
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Stage 1: Token IDs (Rank 2: Batch, Seq)
token_ids = torch.randint(low=0, high=VOCAB_SIZE, size=(BATCH_SIZE, SEQ_LEN), dtype=torch.long, device=DEVICE)
assert token_ids.ndim == 2 and token_ids.dtype == torch.long

# Stage 2: Embeddings (Rank 3: Batch, Seq, Hidden)
embedding_table = torch.randn(VOCAB_SIZE, HIDDEN_DIM, dtype=torch.float32, device=DEVICE)
embeddings = embedding_table[token_ids]
assert embeddings.ndim == 3 and embeddings.shape == (BATCH_SIZE, SEQ_LEN, HIDDEN_DIM)

# Stage 3: Hidden States (Rank 3: Batch, Seq, Hidden)
hidden_states = embeddings + torch.randn_like(embeddings)
assert hidden_states.ndim == 3 and hidden_states.shape == embeddings.shape

# Stage 4: Logits (Rank 3: Batch, Seq, Vocab)
lm_head = torch.randn(HIDDEN_DIM, VOCAB_SIZE, dtype=torch.float32, device=DEVICE)
logits = torch.matmul(hidden_states, lm_head)
assert logits.ndim == 3 and logits.shape == (BATCH_SIZE, SEQ_LEN, VOCAB_SIZE)

print("Forward pass tensors verified successfully.")
