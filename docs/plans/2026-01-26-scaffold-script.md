# Cloudrail Scaffold Script Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add a deterministic bash script that scaffolds the required directory/file tree and run it once.

**Architecture:** The script lives under `tools/` and uses `mkdir -p` and `touch` calls only. Running it from repo root creates the specified directories and empty files without touching existing extraneous files.

**Tech Stack:** Bash (POSIX), git CLI.

### Task 1: Create scaffold script

**Files:**
- Create: `tools/scaffold_repo.sh`

**Step 1:** Create the bash script skeleton with `#!/usr/bin/env bash`, `set -euo pipefail`, and a comment block describing usage.

**Step 2:** In the script, add arrays (or grouped commands) that call `mkdir -p` for every directory specified in the scaffold (custom_skills tree, docs, registries, tools, .github workflows).

**Step 3:** Add grouped `touch` commands for all required files (SKILL.md, REFERENCE.md, etc., plus templates, schemas, policies, scripts, registries, workflow files, wrapper scripts). Ensure paths exactly match the requested structure.

**Step 4:** Make the script executable: `chmod +x tools/scaffold_repo.sh`.

### Task 2: Run scaffold script

**Files:**
- Modify: tree structure (new directories/files)

**Step 1:** From repo root, run `./tools/scaffold_repo.sh` to generate the scaffold.

**Step 2:** Verify directories/files exist via `git status` or `ls` checks.

**Step 3:** Review new files (they will be empty per requirements) and ensure no existing extras were removed.

### Task 3: Commit changes

**Files:**
- `tools/scaffold_repo.sh`
- All newly created directories/files

**Step 1:** Stage everything: `git add tools/scaffold_repo.sh custom_skills docs registries tools .github` (or `git add .`).

**Step 2:** Commit with message `chore: add scaffold script` (or similar).

**Step 3:** Confirm clean working tree via `git status`.

Plan complete and saved to `docs/plans/2026-01-26-scaffold-script.md`. Two execution options:

1. **Subagent-Driven (this session)**
2. **Parallel Session (separate)**

Which approach?
