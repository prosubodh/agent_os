# Compiled Agent OS Governance Prompt
Do NOT deviate from these active rules under any circumstances.

## Governance Rule: zero-assumption
# Zero Assumption Rule
- DIRECTIVE: Do NOT guess specifications or make code design assumptions.
- (MANDATORY: Ask exactly 1-2 targeted clarifying questions on ambiguous specs before writing code.)
- (MANDATORY: Reject or request business value justification for vague feature requests.)
- ATOMIC_SPLIT: Separate large requests into sub-tasks taking < 4 hours of execution.

## Governance Rule: surgical-diffs
# Surgical Diff Rule (Karpathy Clean Code Policy)
- (CRITICAL: Touch and edit ONLY files and lines directly matching requirements. Unrelated adjacent edits are violations.)
- (BANNED: Running auto-formatters or making stylistic adjustments on adjacent, healthy code.)
- VALIDATION: Run `git diff` locally to verify changes are 100% minimal and focused before proposing git commits.

## Governance Rule: testing
# TS Test Mock Safety (Pocock Rules)
- (BANNED: Type assertions like 'as Type' or 'as any' in test mock data objects.)
- (MANDATORY: Use '@total-typescript/shoehorn' helper methods (e.g., 'fromPartial()', 'fromAny()') for partial mock data.)
- COMPILER: This rule triggers JIT expansion ONLY when editing files in test paths.
