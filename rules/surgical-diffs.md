---
name: surgical-diffs
version: 1.2.0
tokens: 38
conflicts_with: []
concepts:
  SURGICAL_EDITS: "CRITICAL: Touch and edit ONLY files and lines directly matching requirements. Unrelated adjacent edits are violations."
  CLEAN_DIFFS: "BANNED: Running auto-formatters or making stylistic adjustments on adjacent, healthy code."
---
# Surgical Diff Rule (Karpathy Clean Code Policy)
- [SURGICAL_EDITS]
- [CLEAN_DIFFS]
- VALIDATION: Run `git diff` locally to verify changes are 100% minimal and focused before proposing git commits.
