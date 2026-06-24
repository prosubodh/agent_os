---
name: ai-intent-classification
version: "1.0.0"
tokens: 150
paths: []
conflicts_with: []
concepts:
  INTENT_CLASS: "Classify AI problem type (Search/Retrieval, Generation/Creation, Classification, Structured Extraction) before designing features."
  RAG_PREFERENCE: "Prefer RAG (Retrieval-Augmented Generation) over fine-tuning for domain-specific or dynamic data. Use fine-tuning only when prompts and retrieval fail."
---
# AI Intent Classification SOP
- [INTENT_CLASS]
- [RAG_PREFERENCE]
- CLASSIFY: Document intent classification and YAGNI validation prior to implementing any ML capability.
