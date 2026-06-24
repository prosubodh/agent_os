---
name: audit-checklist
version: "1.0.0"
tokens: 198
paths: []
conflicts_with: []
concepts:
  SECURITY_AUDIT: "Verify zero hardcoded secrets, input validation, server-side auth, and OWASP coverage."
  SCALABILITY_AUDIT: "Verify stateless design, caching, and absence of single-node bottlenecks."
  ERROR_LOGGING_AUDIT: "Check structured logs, correlation IDs, fail-fast boundary controls, and zero PII exposure."
  YAGNI_PATTERNS_AUDIT: "Enforce anti-pattern prevention (no God objects, spaghetti code) and alignment with DAT."
  TEST_COVERAGE_AUDIT: "Confirm unit tests exist for business logic and integration tests for module boundaries."
---
# Architecture Audit Checklist
- [SECURITY_AUDIT]
- [SCALABILITY_AUDIT]
- [ERROR_LOGGING_AUDIT]
- [YAGNI_PATTERNS_AUDIT]
- [TEST_COVERAGE_AUDIT]
