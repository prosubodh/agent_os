---
name: ai-safety-gate
version: "1.0.0"
tokens: 193
paths: []
conflicts_with: []
concepts:
  PII_SCRUBBING: "Scrub PII and sensitive data from all LLM inputs and prompts."
  OUTPUT_MODERATION: "Deploy output moderation and content filtering for user-facing outputs."
  CIRCUIT_BREAKER: "Define circuit breakers to handle malformed, missing, or failed LLM responses gracefully."
  COST_CONTROL: "Enforce rate limits and cost caps to prevent runway API expenses."
  HITL_GATE: "Require Human-in-the-Loop gates for high-risk actions like deletes, message sends, and payments."
---
# AI Safety and Privacy SOP
- [PII_SCRUBBING]
- [OUTPUT_MODERATION]
- [CIRCUIT_BREAKER]
- [COST_CONTROL]
- [HITL_GATE]
- ACTION: Run the safety checklist and halt development if any gate fails.
