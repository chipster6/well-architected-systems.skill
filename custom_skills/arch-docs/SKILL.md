---
name: arch-docs
version: "1.0"
description: >
  Use when you need to generate, expand, or validate architecture documentation (C4, service catalog/specs, security architecture, threat model, operations model, contracts) from an established baseline.
  Triggers: "arch docs", "architecture docs", "C4 component", "service catalog", "service spec", "threat model", "security architecture", "operations model", "runbook", "contract spec", "Well-Architected mapping", "arch-docs gate", "validate_docs.py".
  Requires baseline gate PASS and fails closed if required policy inputs or docs/architecture/ are missing.
---

# Arch-Docs Skill

## Purpose
Provides architecture documentation generation and validation capabilities. This skill depends on the baseline gate passing and enforces documentation-first methodology for system architecture work.

## References (progressive disclosure)
- `references/executive-summary.md`
- `references/ARCH_DOCS_PHASES.md`

## Core Functionality
- **Architecture Documentation**: Generate and validate system architecture documents
- **Template Management**: Provides standardized templates for architecture artifacts
- **Schema Validation**: Ensures documentation follows established patterns and governance
- **Baseline Dependency**: Blocked until arch-baseline gate passes

## Key Components

### Scripts
- `validate_docs.py` - Main validation script with baseline gate dependency

### Resources
- `resources/templates/` - Templates for architecture documents
- `resources/schemas/` - JSON schemas for validation
- `resources/policy/` - Documentation governance policies

## Required Documents
Creates and validates architecture documents in:
- `docs/architecture/` - System architecture documentation
- `docs/baseline/` - Cross-references baseline artifacts

## Usage
```bash
# Validate architecture documentation (includes baseline gate check)
python custom_skills/arch-docs/scripts/validate_docs.py
```

## Baseline Gate Dependency
This skill **requires** the baseline gate to pass before execution:
- Calls `tools/run_baseline_gate.sh` or direct baseline validator
- If baseline fails: prints "BASELINE GATE FAILED" and exits with code 1
- Only proceeds with documentation work after baseline validation succeeds

## Dependencies
- Python standard library only
- Requires baseline gate to pass
- No network access required

## Governance Role
This skill enforces **documentation-first** methodology:
- All architecture work must be documented before implementation
- Strict validation ensures quality and consistency
- Blocked until baseline architecture foundation is established

## Exit Codes
- `0` - All validations passed
- `1` - Baseline gate failed or documentation validation failed
