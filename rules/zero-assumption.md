---
name: zero-assumption
version: 1.2.0
tokens: 45
conflicts_with: []
concepts:
  CLARIFY_AMBIGUITY: "MANDATORY: Ask exactly 1-2 targeted clarifying questions on ambiguous specs before writing code."
  VALUE_GATE: "MANDATORY: Reject or request business value justification for vague feature requests."
---
# Zero Assumption Rule
- DIRECTIVE: Do NOT guess specifications or make code design assumptions.
- [CLARIFY_AMBIGUITY]
- [VALUE_GATE]
- ATOMIC_SPLIT: Separate large requests into sub-tasks taking < 4 hours of execution.
