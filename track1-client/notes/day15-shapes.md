# Day 15: Tensor Shape, Dtype, and Device

## Transformer Forward Pass Pipeline
1. **Token IDs (`[Batch, Seq_Len]`, `int64`)**: Discrete vocabulary indices. Must strictly be integers.
2. **Embeddings (`[Batch, Seq_Len, Hidden_Dim]`, `float32`)**: Continuous vector lookup per token.
3. **Hidden States (`[Batch, Seq_Len, Hidden_Dim]`, `float32`)**: Post-attention & FFN feature representations. Shape is invariant across transformer layers.
4. **Logits (`[Batch, Seq_Len, Vocab_Size]`, `float32`)**: Unnormalized probability scores mapped back across the entire vocabulary.

## Critical Production Assertions
- Floating-point index prevention on embedding lookup.
- Strict token ID upper-bound assertions (`id < vocab_size`).
- Projection inner dimension alignment (`hidden.shape[-1] == weight.shape[0]`).
- Contiguity checks (`is_contiguous()`) before invoking memory view mutations (`.view()`).
- Device colocation assertions prior to binary operations.
