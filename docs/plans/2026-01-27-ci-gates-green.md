# CI Gates Green Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Get the local wrapper gates passing by creating required directories and filling required policy YAMLs with minimal valid structure.

**Architecture:** The arch-docs and impl-strategy validators in this repo currently enforce baseline-first and only check for existence + non-empty policy files and output directories. We'll add minimal but structured YAML content and create the missing doc roots. Then we will run the three wrapper scripts to confirm PASS.

**Tech Stack:** Shell scripts, Python validators, YAML policy files.

### Task 1: Verify current gate failures (baseline/arch-docs/impl-strategy)

**Files:**
- Modify: none

**Step 1: Run baseline gate**

Run: `./tools/run_baseline_gate.sh`
Expected: PASS (exit 0) or clear failure list to address before continuing.

**Step 2: Run arch-docs gate**

Run: `./tools/run_arch_docs_gate.sh`
Expected (current state): FAIL complaining about missing `docs/architecture/` and/or empty policy files.

**Step 3: Run impl-strategy gate**

Run: `./tools/run_impl_gate.sh`
Expected (current state): FAIL complaining about missing `docs/implementation/` and/or empty `gate_definitions.yml`.

### Task 2: Create canonical output directories required by validators

**Files:**
- Create: `docs/architecture/`
- Create: `docs/implementation/`

**Step 1: Create directories**

Run: `mkdir -p docs/architecture docs/implementation`
Expected: directories exist.

**Step 2: Re-run gates to confirm failures are now only policy related**

Run: `./tools/run_arch_docs_gate.sh && ./tools/run_impl_gate.sh`
Expected: still FAIL (policies), but no longer missing directory errors.

### Task 3: Populate arch-docs policy YAMLs (minimal structured content)

**Files:**
- Modify: `custom_skills/arch-docs/resources/policy/required_sections.yml`
- Modify: `custom_skills/arch-docs/resources/policy/crosslink_rules.yml`
- Modify: `custom_skills/arch-docs/resources/policy/placeholder_rules.yml`

**Step 1: Write minimal required sections policy**

Content should define:
- version
- doc_types with required section headers

**Step 2: Write minimal crosslink rules**

Content should define:
- version
- required anchor targets (baseline index/handoff/adherence plan)

**Step 3: Write minimal placeholder rules**

Content should define:
- version
- disallowed placeholder tokens (fail-closed markers)

**Step 4: Run arch-docs gate**

Run: `./tools/run_arch_docs_gate.sh`
Expected: PASS (exit 0).

### Task 4: Populate impl-strategy gate definitions policy (minimal structured content)

**Files:**
- Modify: `custom_skills/impl-strategy/resources/policy/gate_definitions.yml`

**Step 1: Write minimal gate definitions**

Content should define:
- version
- gate list with ids and required artifacts (docs paths)

**Step 2: Run impl-strategy gate**

Run: `./tools/run_impl_gate.sh`
Expected: PASS (exit 0).

### Task 5: Confirm all wrapper scripts pass locally

**Files:**
- Modify: none

**Step 1: Run all three wrappers**

Run:
`./tools/run_baseline_gate.sh && ./tools/run_arch_docs_gate.sh && ./tools/run_impl_gate.sh`

Expected: all PASS (exit 0).

### Task 6: Commit and push changes (so CI is the continuity anchor)

**Files:**
- Modify/Create: as above

**Step 1: Commit**

Run:
`git add docs/architecture docs/implementation custom_skills/arch-docs/resources/policy/*.yml custom_skills/impl-strategy/resources/policy/gate_definitions.yml`

Then:
`git commit -m "chore: unblock gates (policy yaml + doc dirs)"`

**Step 2: Push**

Run: `git push origin main`
Expected: remote updated, CI can run.

