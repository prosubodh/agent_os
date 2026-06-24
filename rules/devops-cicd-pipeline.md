---
name: devops-cicd-pipeline
version: "1.0.0"
tokens: 126
paths: []
conflicts_with: []
concepts:
  CI_SECTOR_STEPS: "Execute CI jobs strictly in order: install -> lint -> type-check -> test -> build."
  TEST_STEP_BLOCK: "Enforce that pipelines must never skip or override unit and integration test executions."
  IMMUTABLE_ARTIFACTS: "Build identical immutable artifacts from equivalent git commit hashes."
---
# DevOps CI/CD Pipeline SOP
- [CI_SECTOR_STEPS]
- [TEST_STEP_BLOCK]
- [IMMUTABLE_ARTIFACTS]
