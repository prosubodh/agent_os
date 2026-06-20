#!/usr/bin/env bash
# scripts/pre-commit.sh
# Git hook wrapper. Delegates execution to the Python pre-commit pipeline.

set -e
REAL_PATH=$(python3 -c "import os; print(os.path.realpath('$0'))")
SCRIPTS_DIR=$(dirname "$REAL_PATH")

python3 "$SCRIPTS_DIR/pre-commit.py"
