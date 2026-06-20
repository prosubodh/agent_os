#!/usr/bin/env python3
# scripts/check-conflicts.py
# Statically validates that active rules in the manifest do not contradict each other.

import os
import sys
import re

def parse_manifest(manifest_path):
    """Parses rules and local_rules from manifest using regex to avoid yaml dependency."""
    if not os.path.exists(manifest_path):
        print(f"Error: Manifest file {manifest_path} not found.")
        sys.exit(1)
        
    with open(manifest_path, 'r') as f:
        content = f.read()

    rules = []
    # Match standard list format for rules: - name: "rule-name"
    # Or local rules: - path: "rule-path"
    rule_name_matches = re.findall(r'-\s+name:\s+["\']?([\w-]+)["\']?', content)
    local_path_matches = re.findall(r'-\s+path:\s+["\']?([\w\-./]+)["\']?', content)
    
    return rule_name_matches, local_path_matches

def resolve_rule_path(rule_name, project_root):
    """Resolves rule file using Isolated Cache Resolution: local cache overrides global home cache."""
    local_cache_path = os.path.join(project_root, ".agent-os", "cache", "rules", f"{rule_name}.md")
    global_cache_path = os.path.join(os.path.expanduser("~"), ".agent-os", "cache", "rules", f"{rule_name}.md")
    
    # Check project rules folder first (local overrides/compositions)
    local_rules_dir = os.path.join(project_root, ".agent-os", "rules", f"{rule_name}.md")
    if os.path.exists(local_rules_dir):
        return local_rules_dir
        
    # Check if project-local cache exists
    if os.path.exists(local_cache_path):
        return local_cache_path
        
    # Check global cache ONLY if no project rules are present locally
    has_local_rules = os.path.exists(os.path.join(project_root, ".agent-os", "rules")) or os.path.exists(local_cache_path)
    if not has_local_rules and os.path.exists(global_cache_path):
        return global_cache_path
        
    return None

def parse_rule_metadata(rule_path):
    """Extracts name and conflicts_with list from a rule's YAML frontmatter."""
    if not rule_path or not os.path.exists(rule_path):
        return None, []
        
    with open(rule_path, 'r') as f:
        content = f.read()
        
    # Find text between the first two '---'
    frontmatter_match = re.search(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL | re.MULTILINE)
    if not frontmatter_match:
        return None, []
        
    frontmatter = frontmatter_match.group(1)
    
    # Extract name
    name_match = re.search(r'^name:\s*["\']?([\w-]+)["\']?', frontmatter, re.MULTILINE)
    rule_name = name_match.group(1) if name_match else os.path.basename(rule_path).replace(".md", "")
    
    # Extract conflicts_with list
    conflicts = []
    # Match inline list format: conflicts_with: [a, b]
    inline_match = re.search(r'^conflicts_with:\s*\[(.*?)\]', frontmatter, re.MULTILINE)
    if inline_match:
        conflicts = [c.strip().strip('"').strip("'") for c in inline_match.group(1).split(",") if c.strip()]
    else:
        # Match multi-line YAML list format
        list_block_match = re.search(r'^conflicts_with:\s*\n((?:\s+-\s+.*\n?)+)', frontmatter, re.MULTILINE)
        if list_block_match:
            conflicts = re.findall(r'-\s+["\']?([\w-]+)["\']?', list_block_match.group(1))
            
    return rule_name, conflicts

def main():
    scripts_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(scripts_dir)
    manifest_path = os.path.join(project_root, ".agent-os.yaml")
    
    rule_names, local_paths = parse_manifest(manifest_path)
    
    # Map active rules to their resolved file paths
    active_rules = {}
    
    # 1. Load imported rules
    for rname in rule_names:
        rpath = resolve_rule_path(rname, project_root)
        if rpath:
            active_rules[rname] = rpath
        else:
            print(f"Warning: Rule '{rname}' is active in manifest but not found in cache or local rules.")

    # 2. Load local rules
    for lpath in local_paths:
        abs_lpath = os.path.join(project_root, lpath)
        if os.path.exists(abs_lpath):
            rname = os.path.basename(lpath).replace(".md", "")
            active_rules[rname] = abs_lpath
        else:
            print(f"Warning: Local rule path '{lpath}' not found.")

    # Parse metadata for all active rules
    conflict_map = {}
    for rname, rpath in active_rules.items():
        parsed_name, conflicts = parse_rule_metadata(rpath)
        if parsed_name:
            conflict_map[parsed_name] = conflicts

    # Verify conflicts
    conflicts_found = False
    for rname, conflicts in conflict_map.items():
        for conflict in conflicts:
            if conflict in conflict_map:
                print(f"CRITICAL ERROR: Rule Conflict Detected!")
                print(f"  - Active Rule A: '{rname}'")
                print(f"  - Active Rule B: '{conflict}' (declared as incompatible by '{rname}')")
                conflicts_found = True

    if conflicts_found:
        print("Commit aborted due to governance rule conflicts. Please resolve the contradictions in '.agent-os.yaml'.")
        sys.exit(1)
    else:
        print("Success: Rule conflict validation passed. No contradictions found.")
        sys.exit(0)

if __name__ == "__main__":
    main()
