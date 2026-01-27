# Documentation Governance (Baseline)

## Purpose
Define the canonical documentation system-of-record for this repository and the rules that keep architecture work deterministic, auditable, and reviewable.

## Canonical locations
- Baseline (owned by `arch-baseline`): `docs/baseline/`
- Architecture (owned by `arch-docs`): `docs/architecture/`
- Implementation strategy (owned by `impl-strategy`): `docs/implementation/`
- Registries (normalized system-of-record): `registries/`
- Audit logs and run artifacts: `docs/audit/`

No parallel competing doc roots are allowed. If drafts exist elsewhere (e.g. `project-scope/`), they are non-canonical unless explicitly promoted.

## Change control
### Normative changes
Any change that introduces or modifies a normative requirement (MUST/SHALL/REQUIRED) must be traceable to:
- provider framework evidence (captured in the evidence log), or
- an ADR that justifies deviation.

### Baseline invariants
Baseline invariants are owned by `arch-baseline`. Downstream skills must not rewrite baseline invariants without:
1) an ADR, and
2) an update to `docs/baseline/BASELINE_HANDOFF.md`.

## Auditability requirements
### Logs (append-only)
Tools and evidence must be recorded as append-only logs:
- `docs/audit/tool_calls/tool_call_audit.jsonl`
- `docs/audit/evidence/evidence_log.jsonl`

### Human rollups
- `docs/audit/EVIDENCE_LOG.md`
- `docs/audit/tool_calls/TOOL_CALL_AUDIT_SUMMARY.md`

## No-placeholder rule
Repository documentation must not contain placeholder tokens in required sections (e.g., "TODO", "TBD", "FIXME") unless explicitly allowed by policy for that document type.

## Run folders (per execution)
Each skill execution must create a run folder under `docs/audit/<skill>/<run-id>/` containing at minimum:
- `PHASE_COMPLETION_REPORT.md`
- `FILES_CHANGED.md`
- `OPEN_ITEMS.md`
- `QUALITY_GATE_REPORT.md` (when applicable)

