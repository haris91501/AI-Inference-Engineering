import math
import torch
import torch.nn as nn
import torch.nn.functional as F

def trace_multi_head_attention():
    print("=" * 65)
    print(" Day 17: Multi-Head Attention + Causal Masking Trace")
    print("=" * 65)

    batch_size = 2
    seq_len = 4
    d_model = 64
    num_heads = 4
    d_k = d_model // num_heads

    x = torch.randn(batch_size, seq_len, d_model)

    W_q = nn.Linear(d_model, d_model, bias=False)
    W_k = nn.Linear(d_model, d_model, bias=False)
    W_v = nn.Linear(d_model, d_model, bias=False)

    Q = W_q(x).view(batch_size, seq_len, num_heads, d_k).transpose(1, 2)
    K = W_k(x).view(batch_size, seq_len, num_heads, d_k).transpose(1, 2)
    V = W_v(x).view(batch_size, seq_len, num_heads, d_k).transpose(1, 2)

    # 1. Raw scores
    scores = torch.matmul(Q, K.transpose(-2, -1)) / math.sqrt(d_k)
    print(f"[1] Scaled Attention Scores Shape: {list(scores.shape)} -> [B, H, S, S]")

    # 2. Causal Mask (Lower Triangular)
    # torch.tril produces 1s in lower triangle, 0s in upper triangle
    mask = torch.tril(torch.ones(seq_len, seq_len)).view(1, 1, seq_len, seq_len)
    masked_scores = scores.masked_fill(mask == 0, float('-inf'))
    print(f"[2] Causal Mask applied: upper-triangle filled with -inf")

    # 3. Softmax over keys
    causal_weights = F.softmax(masked_scores, dim=-1)
    print(f"[3] Causal Attention Weights (Softmax) Shape: {list(causal_weights.shape)}")

    # 4. Print Head 0 Matrix for Batch 0 to inspect zeroed future tokens
    sample_matrix = causal_weights[0, 0]
    print("\n[Sample Attention Matrix: Batch 0, Head 0]")
    for row_idx, row in enumerate(sample_matrix):
        formatted_row = [f"{val.item():.3f}" for val in row]
        print(f"Token {row_idx} attends to -> {formatted_row}")

    # 5. Context Output
    context = torch.matmul(causal_weights, V)
    context = context.transpose(1, 2).contiguous().view(batch_size, seq_len, d_model)
    W_o = nn.Linear(d_model, d_model, bias=False)
    out = W_o(context)
    print(f"\n[4] Final Projected Output Shape: {list(out.shape)} -> [B, S, D]")

    # 6. Strict Verification
    assert out.shape == (batch_size, seq_len, d_model), "Output shape mismatch!"
    assert sample_matrix[0, 1].item() == 0.0, "Causal mask failed: Token 0 attended to Token 1!"
    print("\n[VERIFICATION STATUS]: PASSED - Causal masking & output projection verified.")

if __name__ == "__main__":
    trace_multi_head_attention()
