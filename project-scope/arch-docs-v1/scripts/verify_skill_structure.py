#!/usr/bin/env python3
import os
import sys

REQUIRED_DIRS = [
    "references",
    "templates",
    "schemas",
    "checks",
    "scripts",
    os.path.join("assets", "examples"),
]

REQUIRED_FILES = [
    "SKILL.md",
    "AGENTS.md",
    os.path.join("references", "workflow.md"),
    os.path.join("references", "document-selection.md"),
    os.path.join("references", "reference-policy.md"),
    os.path.join("references", "quality-gates.md"),
    os.path.join("references", "mcp-validation.md"),
    os.path.join("references", "templates.md"),
    os.path.join("checks", "lint-skill.sh"),
    os.path.join("checks", "regex-gates.txt"),
    os.path.join("checks", "required-sections.yml"),
    os.path.join("scripts", "verify_skill_structure.py"),
    os.path.join("scripts", "validate_skill_artifacts.py"),
    os.path.join("schemas", "mcp_evidence_log.schema.json"),
    os.path.join("schemas", "phase_completion_report.schema.json"),
    os.path.join("schemas", "well_architected_pillar_matrix.schema.json"),
    os.path.join("schemas", "claim_index.schema.json"),
    os.path.join("assets", "examples", "MCP_EVIDENCE_LOG.example.md"),
    os.path.join("assets", "examples", "WELL_ARCHITECTED_PILLAR_MATRIX.example.md"),
    os.path.join("assets", "examples", "PHASE_COMPLETION_REPORT_P0.example.md"),
]

def main():
    root = os.path.dirname(os.path.abspath(__file__))
    root = os.path.normpath(os.path.join(root, os.pardir))
    missing = []

    for d in REQUIRED_DIRS:
        if not os.path.isdir(os.path.join(root, d)):
            missing.append(f"missing directory: {d}")

    for f in REQUIRED_FILES:
        if not os.path.isfile(os.path.join(root, f)):
            missing.append(f"missing file: {f}")

    if missing:
        for m in missing:
            print(m)
        sys.exit(1)

    print("verify_skill_structure: PASS")


if __name__ == "__main__":
    main()
