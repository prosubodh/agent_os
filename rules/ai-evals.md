---
name: ai-evals
version: "1.0.0"
tokens: 143
paths: []
conflicts_with: []
concepts:
  GOLD_STANDARD: "Establish a gold standard dataset of 20-50 verified input-output pairs representing ideal behavior."
  EVAL_METRICS: "Track Faithfulness, Relevance, Latency (P50/P95), and cost-per-query."
  PASS_THRESHOLDS: "Set minimum metric thresholds; fail build/deploy if thresholds are not met."
  RE_EVALUATION: "Re-run evaluation sets after every prompt update or model upgrade."
---
# AI Evaluation SOP
- [GOLD_STANDARD]
- [EVAL_METRICS]
- [PASS_THRESHOLDS]
- [RE_EVALUATION]
