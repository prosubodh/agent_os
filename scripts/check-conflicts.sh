#!/usr/bin/env bash
# scripts/check-conflicts.sh
# Bash wrapper around conflict detector Python script.

set -e
REAL_PATH=$(python3 -c "import os; print(os.path.realpath('$0'))")
SCRIPTS_DIR=$(dirname "$REAL_PATH")

python3 "$SCRIPTS_DIR/check-conflicts.py"
