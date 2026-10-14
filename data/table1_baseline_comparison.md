| Compliance Checking Method | Paradigm | Precision | Recall | F1 Score | Accuracy | Life-Safety FN | Latency / Case |
|:---------------------------|:---------|:---------:|:------:|:--------:|:--------:|:--------------:|:--------------:|
| **ASTG Deterministic Oracle (Ours)** | Symbolic Graph | 1.000 | 1.000 | 1.000 | 1.000 | 0 [PASS] | 0.1 ms |
| **Chain-of-Thought LLM (Few-Shot GPT-4o)** | LLM | 1.000 | 0.889 | 0.941 | 0.944 | 0 [PASS] | 1.99 s |
| **Vanilla LLM (Zero-Shot GPT-4o)** | LLM | 0.857 | 0.667 | 0.750 | 0.778 | **2** [FAIL] | 1.02 s |
| **Simplified Heuristic Baseline** | Heuristic | 1.000 | 1.000 | 1.000 | 1.000 | 0 [PASS] | 6.5 ms |