#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

pass=true

# Check frontmatter in SKILL.md
if ! awk 'NR==1{print}' SKILL.md | grep -q '^---$'; then
  echo "[lint] SKILL.md missing YAML frontmatter start"; pass=false; fi
if ! awk 'NR==2{print}' SKILL.md | grep -q '^name: cloudrail-arch-docs$'; then
  echo "[lint] SKILL.md frontmatter missing name cloudrail-arch-docs"; pass=false; fi
if ! awk 'NR==3{print}' SKILL.md | grep -q '^description: '; then
  echo "[lint] SKILL.md frontmatter missing description"; pass=false; fi

# Naming check for phase reports (allow P0-P6 and PN template reference)
if grep -R "PHASE_COMPLETION_REPORT_" -n . --exclude="lint-skill.sh" --exclude="*.skill" | grep -Ev 'PHASE_COMPLETION_REPORT_P([0-6]|N)'; then
  echo "[lint] Found non-canonical phase report naming"; pass=false; fi

# Evidence id rule in reference-policy
if ! grep -q "MCP-YYYYMMDD-NNNN" references/reference-policy.md; then
  echo "[lint] evidence_id format missing in reference-policy"; pass=false; fi

# TOKEN gate present
if ! grep -q "TOKEN_REPLACEMENT_GATE" references/quality-gates.md; then
  echo "[lint] TOKEN_REPLACEMENT_GATE missing"; pass=false; fi

# GOV-ARCH-001 update rule in document-selection
if ! grep -q "GOV-ARCH-001" references/document-selection.md; then
  echo "[lint] GOV-ARCH-001 rule missing"; pass=false; fi

$pass && echo "lint-skill: PASS" || { echo "lint-skill: FAIL"; exit 1; }
