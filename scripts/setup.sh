#!/usr/bin/env bash
# scripts/setup.sh
# Bootstraps the local Git repository to link the Agent OS pre-commit hook.

set -e

# 1. Locate Git root directory
GIT_DIR=$(git rev-parse --git-dir 2>/dev/null)
if [ -z "$GIT_DIR" ]; then
  echo "Error: Not a git repository. Run 'git init' first."
  exit 1
fi

PROJECT_ROOT=$(git rev-parse --show-toplevel)
SCRIPTS_DIR="$PROJECT_ROOT/scripts"
HOOKS_DIR="$GIT_DIR/hooks"
CACHE_DIR="$PROJECT_ROOT/.agent-os/cache"

echo "=== Initializing Agent OS Setup ==="

# 2. Make all script files executable
chmod +x "$SCRIPTS_DIR"/pre-commit.sh
chmod +x "$SCRIPTS_DIR"/check-conflicts.sh
chmod +x "$SCRIPTS_DIR"/compiler.sh

# 3. Establish symbolic link for pre-commit hook
PRE_COMMIT_HOOK="$HOOKS_DIR/pre-commit"

if [ -L "$PRE_COMMIT_HOOK" ] || [ -f "$PRE_COMMIT_HOOK" ]; then
  echo "Warning: Existing pre-commit hook found. Backing up to pre-commit.backup..."
  mv "$PRE_COMMIT_HOOK" "$PRE_COMMIT_HOOK.backup"
fi

ln -s "$SCRIPTS_DIR/pre-commit.sh" "$PRE_COMMIT_HOOK"
echo "Success: Symbolic link created from $PRE_COMMIT_HOOK to scripts/pre-commit.sh"

# 4. Create project local cache and ensure gitignore hygiene
mkdir -p "$CACHE_DIR"
GITIGNORE="$PROJECT_ROOT/.gitignore"

if [ -f "$GITIGNORE" ]; then
  if ! grep -q ".agent-os/cache" "$GITIGNORE"; then
    echo -e "\n# Agent OS Cache\n.agent-os/cache" >> "$GITIGNORE"
    echo "Added .agent-os/cache to .gitignore"
  fi
else
  echo -e "# Agent OS Cache\n.agent-os/cache" > "$GITIGNORE"
  echo "Created .gitignore and added .agent-os/cache"
fi

echo "=== Setup Complete. Agent OS is now active! ==="
