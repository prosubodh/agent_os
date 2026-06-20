#!/usr/bin/env python3
# scripts/pre-commit.py
# Pre-commit hook validator. Automatically resolves conflicts, JIT compiles prompts, 
# and runs the language-agnostic validation shell commands specified in the manifest.

import os
import sys
import subprocess
import re

def parse_pre_commit_commands(manifest_path):
    """Parses custom shell validation commands under hooks.pre-commit block."""
    if not os.path.exists(manifest_path):
        return []
        
    with open(manifest_path, 'r') as f:
        content = f.read()
        
    # Find the hooks section
    hooks_match = re.search(r'^hooks:\s*\n((?:\s+.*\n?)+)', content, re.MULTILINE)
    if not hooks_match:
        return []
        
    hooks_block = hooks_match.group(1)
    
    # Find pre-commit subsection within hooks
    pre_commit_match = re.search(r'^\s+pre-commit:\s*\n((?:\s+.*\n?)+)', hooks_block, re.MULTILINE)
    if not pre_commit_match:
        return []
        
    pre_commit_block = pre_commit_match.group(1)
    
    # Parse list of commands: - name: "...", run: "..."
    commands = []
    # Match blocks like: - name: "X"\n  run: "Y"
    command_entries = re.findall(r'-\s+name:\s+["\']?(.*?)["\']?\n\s+run:\s+["\']?(.*?)["\']?\n', pre_commit_block)
    for name, run_cmd in command_entries:
        commands.append({
            "name": name.strip(),
            "run": run_cmd.strip()
        })
        
    return commands

def main():
    scripts_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(scripts_dir)
    manifest_path = os.path.join(project_root, ".agent-os.yaml")
    
    # 1. Run Conflict Detector
    print("Checking for governance conflicts...")
    conflict_res = subprocess.run([sys.executable, os.path.join(scripts_dir, "check-conflicts.py")], cwd=project_root)
    if conflict_res.returncode != 0:
        print("Pre-commit hook aborted: Conflict detected.")
        sys.exit(1)
        
    # 2. Run JIT Compiler
    print("\nCompiling JIT Prompt rules...")
    compiler_res = subprocess.run([sys.executable, os.path.join(scripts_dir, "compiler.py")], cwd=project_root)
    if compiler_res.returncode != 0:
        print("Pre-commit hook aborted: Prompt compiler failed.")
        sys.exit(1)

    # 3. Read and execute Quality Gates
    gates = parse_pre_commit_commands(manifest_path)
    if not gates:
        print("\nNo custom quality gates defined in '.agent-os.yaml'. Skipping verification.")
        sys.exit(0)
        
    print(f"\nRunning {len(gates)} Quality Gate validation check(s)...")
    for gate in gates:
        name = gate["name"]
        cmd = gate["run"]
        print(f"-> Gate [{name}]: Executing '{cmd}'...")
        
        # Execute command in project root
        res = subprocess.run(cmd, shell=True, cwd=project_root)
        if res.returncode != 0:
            print(f"\nCRITICAL ERROR: Quality Gate '{name}' failed (Exit code: {res.returncode}).")
            print("Git commit aborted. Please fix the violations before committing.")
            sys.exit(1)
            
    print("\nSuccess: All quality gates passed! Commit allowed.")
    sys.exit(0)

if __name__ == "__main__":
    main()
