---
name: testing
version: 1.2.0
tokens: 42
paths: ["**/*.test.ts", "**/*.spec.ts", "**/tests/**"]
conflicts_with: []
concepts:
  POCOCK_MOCK: "BANNED: Type assertions like 'as Type' or 'as any' in test mock data objects."
  TS_SHOEHORN: "MANDATORY: Use '@total-typescript/shoehorn' helper methods (e.g., 'fromPartial()', 'fromAny()') for partial mock data."
---
# TS Test Mock Safety (Pocock Rules)
- [POCOCK_MOCK]
- [TS_SHOEHORN]
- COMPILER: This rule triggers JIT expansion ONLY when editing files in test paths.
