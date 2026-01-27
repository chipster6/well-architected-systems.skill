---
name: impl-strategy
version: "1.0"
description: >
  Use when you need to turn baseline + architecture docs into an executable implementation strategy: phased plan, dependency DAG (TASK_DAG.json), task catalog, and optional worktree/parallelization plan.
  Triggers: "implementation strategy", "implementation plan", "delivery roadmap", "workstream plan", "task DAG", "dependency graph", "phase plan", "milestones", "worktree plan", "impl gate", "validate_task_graph.py".
  Requires baseline gate PASS and docs/implementation/; fails closed if required policy inputs are missing.
---

# Impl-Strategy Skill

## Purpose
Provides implementation strategy and task graph validation for system development. This skill depends on both baseline gate passing and architecture documentation being in place.

## References (progressive disclosure)
- `references/executive-summary.md`
- `references/IMPL_STRATEGY_PHASES.md`

## Core Functionality
- **Implementation Strategy**: Generate and validate implementation plans and task graphs
- **Task Graph Validation**: Ensure implementation dependencies are properly defined
- **Strategy Documentation**: Create detailed implementation roadmaps
- **Baseline Dependency**: Blocked until arch-baseline gate passes

## Key Components

### Scripts
- `validate_task_graph.py` - Main validation script with baseline gate dependency

### Resources
- `resources/templates/` - Templates for implementation strategy documents
- `resources/schemas/` - JSON schemas for task graph validation
- `resources/policy/` - Implementation governance policies

## Required Documents
Creates and validates implementation artifacts in:
- `docs/implementation/` - Implementation strategy and task graphs
- `docs/baseline/` - Cross-references baseline artifacts
- `docs/architecture/` - Links to architecture documentation

## Usage
```bash
# Validate implementation strategy (includes baseline gate check)
python custom_skills/impl-strategy/scripts/validate_task_graph.py
```

## Baseline Gate Dependency
This skill **requires** baseline gate to pass before execution:
- Calls `tools/run_baseline_gate.sh` or direct baseline validator
- If baseline fails: prints "BASELINE GATE FAILED" and exits with code 1
- Only proceeds with implementation work after baseline validation succeeds

## Dependencies
- Python standard library only
- Requires baseline gate to pass
- Expects architecture documentation to exist
- No network access required

## Governance Role
This skill enforces **implementation-first governance**:
- Implementation strategy must be documented before coding
- Task graphs ensure dependency awareness and proper sequencing
- Blocked until baseline architecture foundation is established

## Exit Codes
- `0` - All validations passed
- `1` - Baseline gate failed or implementation strategy validation failed
