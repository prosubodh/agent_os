#!/usr/bin/env python3
# scripts/compiler.py
# JIT compiles the active governance rules by checking the Git diff, 
# expanding triggered concept anchors, and pruning unused rules (Tree-Shaking).

import os
import sys
import re
import subprocess
import fnmatch

def parse_manifest(manifest_path):
    """Parses rules, local_rules, and token_budget from manifest."""
    if not os.path.exists(manifest_path):
        print(f"Error: Manifest file {manifest_path} not found.")
        sys.exit(1)
        
    with open(manifest_path, 'r') as f:
        content = f.read()

    rules = []
    rule_name_matches = re.findall(r'-\s+name:\s+["\']?([\w-]+)["\']?', content)
    local_path_matches = re.findall(r'-\s+path:\s+["\']?([\w\-./]+)["\']?', content)
    
    # Extract token budget
    budget_match = re.search(r'token_budget:\s*(\d+)', content)
    token_budget = int(budget_match.group(1)) if budget_match else 1000
    
    return rule_name_matches, local_path_matches, token_budget

def get_modified_files(project_root):
    """Gets lists of staged and unstaged modified files from Git."""
    try:
        # Staged files
        staged = subprocess.check_output(
            ["git", "diff", "--name-only", "--cached"], cwd=project_root
        ).decode("utf-8").splitlines()
        # Unstaged files
        unstaged = subprocess.check_output(
            ["git", "diff", "--name-only"], cwd=project_root
        ).decode("utf-8").splitlines()
        
        # Combine and remove empty
        files = list(set([f.strip() for f in (staged + unstaged) if f.strip()]))
        return files
    except Exception as e:
        # Fallback if git fails or is not initialized
        return []

def resolve_rule_path(rule_name, project_root):
    """Resolves rule path following Isolated Cache Resolution."""
    local_rules_dir = os.path.join(project_root, ".agent-os", "rules", f"{rule_name}.md")
    local_cache_path = os.path.join(project_root, ".agent-os", "cache", "rules", f"{rule_name}.md")
    global_cache_path = os.path.join(os.path.expanduser("~"), ".agent-os", "cache", "rules", f"{rule_name}.md")
    
    if os.path.exists(local_rules_dir):
        return local_rules_dir
    if os.path.exists(local_cache_path):
        return local_cache_path
        
    has_local_rules = os.path.exists(os.path.join(project_root, ".agent-os", "rules")) or os.path.exists(local_cache_path)
    if not has_local_rules and os.path.exists(global_cache_path):
        return global_cache_path
        
    return None

def parse_rule_file(rule_path):
    """Parses frontmatter metadata, content, and local concept dictionary from a rule file."""
    if not rule_path or not os.path.exists(rule_path):
        return {}, "", {}
        
    with open(rule_path, 'r') as f:
        content = f.read()
        
    frontmatter = {}
    rule_body = content
    concepts = {}
    
    # Extract frontmatter
    frontmatter_match = re.search(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL | re.MULTILINE)
    if frontmatter_match:
        fm_text = frontmatter_match.group(1)
        rule_body = content[frontmatter_match.end():]
        
        # Extract title/name
        name_match = re.search(r'^name:\s*["\']?([\w-]+)["\']?', fm_text, re.MULTILINE)
        if name_match:
            frontmatter['name'] = name_match.group(1)
            
        # Extract target paths filter
        paths_match = re.search(r'^paths:\s*\[(.*?)\]', fm_text, re.MULTILINE)
        if paths_match:
            frontmatter['paths'] = [p.strip().strip('"').strip("'") for p in paths_match.group(1).split(",") if p.strip()]
        else:
            # Multi-line paths list
            list_match = re.search(r'^paths:\s*\n((?:\s+-\s+.*\n?)+)', fm_text, re.MULTILINE)
            if list_match:
                frontmatter['paths'] = re.findall(r'-\s+["\']?(.*?)["\']?\n', list_match.group(1))

        # Extract tokens metric
        tokens_match = re.search(r'^tokens:\s*(\d+)', fm_text, re.MULTILINE)
        if tokens_match:
            frontmatter['tokens'] = int(tokens_match.group(1))

        # Extract inline concepts
        concept_block_match = re.search(r'^concepts:\s*\n((?:\s+[\w_-]+:\s+.*\n?)+)', fm_text, re.MULTILINE)
        if concept_block_match:
            for line in concept_block_match.group(1).splitlines():
                if ":" in line:
                    k, v = line.split(":", 1)
                    concepts[k.strip()] = v.strip().strip('"').strip("'")
                    
    return frontmatter, rule_body, concepts

def match_paths(modified_files, path_patterns):
    """Returns True if any modified file matches any pattern."""
    if not path_patterns:
        return True # Trigger globally if no path specified
    for f in modified_files:
        for p in path_patterns:
            if fnmatch.fnmatch(f, p):
                return True
    return False

def count_tokens(text):
    """Calculates rough token count (4 characters = 1 token metric)."""
    return len(text) // 4

def main():
    scripts_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(scripts_dir)
    manifest_path = os.path.join(project_root, ".agent-os.yaml")
    
    rule_names, local_paths, token_budget = parse_manifest(manifest_path)
    modified_files = get_modified_files(project_root)
    
    active_rules_content = []
    concept_dictionary = {}
    total_statically_measured_tokens = 0
    
    # 1. Resolve and Load rules
    rules_to_process = []
    for rname in rule_names:
        rpath = resolve_rule_path(rname, project_root)
        if rpath:
            rules_to_process.append(rpath)
    for lpath in local_paths:
        abs_lpath = os.path.join(project_root, lpath)
        if os.path.exists(abs_lpath):
            rules_to_process.append(abs_lpath)
            
    # Process files
    for rpath in rules_to_process:
        metadata, body, concepts = parse_rule_file(rpath)
        path_patterns = metadata.get('paths', [])
        
        # JIT Tree-Shaking filter
        if match_paths(modified_files, path_patterns):
            active_rules_content.append((metadata.get('name', 'rule'), body))
            concept_dictionary.update(concepts)
            total_statically_measured_tokens += metadata.get('tokens', count_tokens(body))
        else:
            # Tree-shaken
            pass
            
    # 2. Expand Concept Anchors JIT
    compiled_body = ""
    for rname, body in active_rules_content:
        # Find all anchors in the format [CONCEPT_NAME]
        anchors = re.findall(r'\[([\w_-]+)\]', body)
        expanded_body = body
        for anchor in anchors:
            if anchor in concept_dictionary:
                # Replace anchor with its SDM definition
                expanded_body = expanded_body.replace(f"[{anchor}]", f"({concept_dictionary[anchor]})")
            else:
                # Keep it as warning or unresolved
                pass
        compiled_body += f"\n## Governance Rule: {rname}\n{expanded_body.strip()}\n"

    # Write compiled prompt
    compiled_dir = os.path.join(project_root, ".agent-os")
    os.makedirs(compiled_dir, exist_ok=True)
    compiled_path = os.path.join(compiled_dir, "compiled_prompt.md")
    
    with open(compiled_path, 'w') as f:
        f.write("# Compiled Agent OS Governance Prompt\n")
        f.write("Do NOT deviate from these active rules under any circumstances.\n")
        f.write(compiled_body)
        
    print("=== Agent OS JIT Prompt Compilation ===")
    print(f"Active Files Staged/Modified: {len(modified_files)}")
    print(f"Active Rules Compiled: {len(active_rules_content)}")
    print(f"Total Statically Measured Tokens: {total_statically_measured_tokens}")
    print(f"Token Budget: {token_budget}")
    print(f"Output: {compiled_path}")
    
    if total_statically_measured_tokens > token_budget:
        print(f"\nWARNING: Aggregate prompt weight ({total_statically_measured_tokens} tokens) exceeds target budget ({token_budget} tokens).")
        print("Consider refining active rules or increasing 'token_budget' in '.agent-os.yaml'.\n")
        
    sys.exit(0)

if __name__ == "__main__":
    main()
