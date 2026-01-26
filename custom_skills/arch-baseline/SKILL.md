# Arch-Baseline Skill

## Purpose
Provides baseline validation and gating for well-architected system documentation. This skill enforces that foundational architectural artifacts exist and meet quality standards before allowing further documentation or implementation work.

## Core Functionality
- **Well-Architected Validation**: Validates adherence plans against strict schema and content requirements
- **Baseline Gate**: Enforces presence and quality of required baseline documents
- **Template Management**: Provides standardized templates for baseline artifacts
- **Schema Enforcement**: JSON schemas ensure document structure and data integrity

## Key Components

### Scripts
- `validate_well_architected.py` - Validates Well-Architected Adherence Plan documents
- `validate_baseline.py` - Wrapper that validates all required baseline outputs

### Resources
- `resources/templates/baseline/WELL_ARCHITECTED_ADHERENCE_PLAN.md` - Template for Well-Architected adherence plans
- `resources/schemas/well_architected_adherence_plan.schema.json` - JSON schema for validation

## Required Baseline Outputs
The baseline gate requires these files to exist and pass validation:
- `docs/baseline/WELL_ARCHITECTED_ADHERENCE_PLAN.md` (validated against schema)
- `docs/baseline/SYSTEM_CHARTER.md` (existence check)
- `docs/baseline/C4_Context.md` (existence check)
- `docs/baseline/C4_Container.md` (existence check)
- `docs/baseline/CLOUD_PROVIDER_DECISION_ADR.md` (existence check)

## Usage
```bash
# Run baseline gate validation
python custom_skills/arch-baseline/scripts/validate_baseline.py

# Or use the wrapper script
./tools/run_baseline_gate.sh
```

## Dependencies
- Python standard library only
- No network access required
- YAML parsing via built-in modules

## Governance Role
This skill serves as the **baseline gate** - it must pass before any other skills (arch-docs, impl-strategy) can execute. This ensures foundational architecture work is complete and validated before proceeding.

## Exit Codes
- `0` - All validations passed
- `1` - Validation failed (missing files, invalid content, placeholders, etc.)