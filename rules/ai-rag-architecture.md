---
name: ai-rag-architecture
version: "1.0.0"
tokens: 199
paths: []
conflicts_with: []
concepts:
  CHUNKING_STRATEGY: "Select chunk size based on content type: 256-512 tokens for dense text, larger for source code."
  EMBEDDING_SELECTION: "Select embedding models based on targeted language, scale, and domain."
  VECTOR_STORE: "Scale vector store based on maturity: local/in-memory for prototypes, managed services for production."
  HYBRID_SEARCH: "Implement hybrid search (dense semantic + sparse lexical) rather than pure vector similarity search."
  COGNITIVE_FIREWALL: "Strip PII and sensitive data from all content before embedding or sending to LLM APIs."
---
# AI RAG Architecture SOP
- [CHUNKING_STRATEGY]
- [EMBEDDING_SELECTION]
- [VECTOR_STORE]
- [HYBRID_SEARCH]
- [COGNITIVE_FIREWALL]
