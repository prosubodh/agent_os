#!/usr/bin/env bash
# scripts/compiler.sh
# Bash wrapper around prompt compiler Python script.

set -e
REAL_PATH=$(python3 -c "import os; print(os.path.realpath('$0'))")
SCRIPTS_DIR=$(dirname "$REAL_PATH")

python3 "$SCRIPTS_DIR/compiler.py"
