# Executive Summary — arch-docs

## Mission
Convert the published baseline (arch-baseline) into a complete, internally consistent, Well-Architected-governed architecture documentation set, using deterministic gates and auditable evidence capture for all normative claims.

This skill is multi-cloud capable. The baseline selects the active cloud provider (AWS/Azure/GCP) and records the governing framework and pillar set in:
- `docs/baseline/WELL_ARCHITECTED_ADHERENCE_PLAN.md`

arch-docs MUST conform to that selected provider framework for all “Well-Architected” mappings.

## Scope (what arch-docs does)
- Expands baseline into full architecture documentation:
  - C4 deepening: Context/Container from baseline + Component-level documentation where applicable
  - Service/container specs and responsibilities
  - Security architecture and threat model
  - Operational readiness artifacts (runbooks, observability expectations)
  - Contract-first artifacts (schemas + examples) where the system exposes APIs/events/data contracts
- Enforces governance:
  - required sections per doc type
  - crosslink rules to baseline and decision records
  - placeholder policy (fail-closed where required)

## Out of scope
- Selecting the cloud provider or changing baseline invariants (baseline owns it).
- Creating implementation task DAG/worktrees (impl-strategy owns it).
- Performing implementation work (coding/IaC) beyond documentation artifacts unless explicitly requested.

## Determinism & Auditability Model
### Baseline-first and fail-closed
- arch-docs MUST not proceed if the baseline gate fails.
- arch-docs MUST fail-closed if required policies are missing/empty or if required output directories do not exist.

Validator entrypoint (current repo):
- `python custom_skills/arch-docs/scripts/validate_docs.py`
- Wrapper: `./tools/run_arch_docs_gate.sh`

### Evidence discipline (normative claims)
A “normative claim” is any statement using MUST/SHALL/REQUIRED or a prescriptive standard.

For each normative claim, arch-docs MUST either:
1) link the claim to an existing evidence record produced during baseline research, OR
2) append a new evidence record and tool-call audit record, OR
3) label the claim `UNVERIFIED EXTERNALLY` with an explicit reason and a follow-up plan.

Canonical audit substrate (repo):
- `docs/audit/tool_calls/tool_call_audit.jsonl`
- `docs/audit/evidence/evidence_log.jsonl`
- Human rollups:
  - `docs/audit/EVIDENCE_LOG.md`
  - `docs/audit/tool_calls/TOOL_CALL_AUDIT_SUMMARY.md`

### Determinism boundary
arch-docs is deterministic relative to:
- the baseline manifest + handoff + adherence plan
- the current repo policy files (required sections/crosslinks/placeholders)
- the evidence snapshot present in the audit logs

If arch-docs performs new external lookups, those lookups MUST be recorded as explicit new inputs (tool-call audit + evidence entries). Determinism is preserved by treating evidence as versioned inputs, not as implicit “current truth.”

## Primary Inputs (hard dependencies)
Minimum required before starting arch-docs:
- Baseline gate PASS (`./tools/run_baseline_gate.sh`)
- Baseline docs:
  - `docs/baseline/BASELINE_INDEX.md`
  - `docs/baseline/BASELINE_HANDOFF.md`
  - `docs/baseline/baseline_manifest.json`
  - `docs/baseline/WELL_ARCHITECTED_ADHERENCE_PLAN.md`
- Registries exist (baseline manifest enumerates them):
  - `registries/constraints_registry.yml`
  - `registries/security_controls_catalog.yml`
  - `registries/slo_catalog.yml`
- Audit logs exist (paths defined in baseline manifest):
  - `docs/audit/evidence/evidence_log.jsonl`
  - `docs/audit/tool_calls/tool_call_audit.jsonl`

## Primary Outputs (mandatory doc families)
arch-docs produces documentation under repo canonical locations (baseline manifest paths):
- Architecture docs: `docs/architecture/`
- Optional contract family (if the system has contracts): `docs/contracts/` + `contracts/schemas/` + `contracts/examples/`
- Decision records (if new design decisions are required): `docs/decisions/` (ADR/RFC)

Minimum architecture set for an initial arch-docs pass:
- Architecture overview
- C4 Component documentation (baseline already includes Context/Container)
- Service specs for each container/service boundary
- Threat model
- Runbook skeleton(s) for material services
- Well-Architected pillar mapping matrix (provider-specific pillar set from baseline adherence plan)

## Run Continuity (stop losing context between sessions)
Each arch-docs run MUST create a run folder:
- `docs/audit/arch-docs/<run-id>/`

Minimum run artifacts:
- `DOC_INVENTORY.md` (what you intend to produce, and what exists)
- `CLAIM_CLASSIFICATION.md` (normative vs descriptive vs unknown)
- `QUALITY_GATE_REPORT.md` (what passed/failed and why)
- `PHASE_COMPLETION_REPORT.md` (what changed, decisions, evidence ids)
- `OPEN_ITEMS.md` (carry-forward items)

Run-id convention:
`RUN-YYYYMMDD-HHMM-arch-docs-<short-slug>`

## Known Current Repo Preconditions (you must satisfy to pass gates)
The current arch-docs validator requires:
- `docs/architecture/` directory exists
- these policy files exist and are non-empty:
  - `custom_skills/arch-docs/resources/policy/required_sections.yml`
  - `custom_skills/arch-docs/resources/policy/crosslink_rules.yml`
  - `custom_skills/arch-docs/resources/policy/placeholder_rules.yml`
