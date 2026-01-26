# Baseline Gate Hardening Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Ensure baseline consumption artifacts, audit templates, and manifest-enforced gate checks exist so the baseline validator fails closed.

**Architecture:** Create template documents and JSON manifest under `docs/baseline` and `docs/audit`, then update the Python validator to require those artifacts’ presence based on manifest references.

**Tech Stack:** Bash, Python standard library, git.

### Task 1: Add baseline consumption artifacts

**Files:**
- Create/modify: `docs/baseline/BASELINE_INDEX.md`, `docs/baseline/BASELINE_HANDOFF.md`

**Steps:**
1. Create/verify `docs/baseline/` directory exists.
2. Write `BASELINE_INDEX.md` using the provided template (no placeholders like TBD/{{}}; leave fields blank).
3. Write `BASELINE_HANDOFF.md` using the provided template (same placeholder rule).

### Task 2: Add audit structure + templates

**Files:**
- Create directories: `docs/audit/evidence`, `docs/audit/tool_calls`
- Create files: `docs/audit/EVIDENCE_LOG.md`, `docs/audit/evidence/evidence_log.jsonl`, `docs/audit/tool_calls/tool_call_audit.jsonl`, `docs/audit/tool_calls/TOOL_CALL_AUDIT_SUMMARY.md`

**Steps:**
1. Run `mkdir -p docs/audit/evidence docs/audit/tool_calls`.
2. Populate `EVIDENCE_LOG.md` with table structure (empty rows allowed).
3. Create empty JSONL files for evidence log and tool-call audit; the templates can be blank lines or single empty objects per instructions.
4. Create `TOOL_CALL_AUDIT_SUMMARY.md` with table structure only.

### Task 3: Create machine-readable manifest

**Files:**
- Create: `docs/baseline/baseline_manifest.json`

**Steps:**
1. Use the provided manifest template (ensure valid JSON; no comments).
2. Ensure artifact entries list all mandatory baseline files and registries.

### Task 4: Ensure baseline index & handoff reference audit + manifest paths

**Files:**
- Modify: `docs/baseline/BASELINE_INDEX.md`
- Modify: `docs/baseline/BASELINE_HANDOFF.md`

**Steps:**
1. Update sections to explicitly mention `docs/baseline/baseline_manifest.json`, `docs/audit/evidence/evidence_log.jsonl`, `docs/audit/tool_calls/tool_call_audit.jsonl`, and `registries/*.yml`.

### Task 5: Update baseline validator

**Files:**
- Modify: `custom_skills/arch-baseline/scripts/validate_baseline.py`

**Steps:**
1. Parse `docs/baseline/baseline_manifest.json` (standard library json module); fail if missing/invalid.
2. Ensure `BASELINE_INDEX.md` and `BASELINE_HANDOFF.md` exist.
3. Ensure audit paths `docs/audit/evidence/evidence_log.jsonl` and `docs/audit/tool_calls/tool_call_audit.jsonl` exist.
4. For each registry listed in manifest (constraints, security controls, slo), ensure file exists.
5. Only check for existence/JSON validity; do not inspect content beyond no placeholders already enforced elsewhere.

### Task 6: Verification commands

**Steps:**
1. Run `bash -n tools/run_baseline_gate.sh`.
2. Run `./tools/run_baseline_gate.sh` and capture output (expect failure until blank templates replaced, but should fail for missing artifact reason, not manifest error).

### Task 7: Commit changes

**Steps:**
1. Stage all modified files.
2. Commit with message `Add baseline index/handoff and audit templates; enforce manifest-based baseline gate`.
