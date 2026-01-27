# Executive Summary — impl-strategy

## Mission
Transform baseline + architecture documentation into an implementation strategy that is executable:
- a dependency-aware task DAG
- a phase plan with entry/exit gates
- an optional parallelization/worktree plan
- audit-grade traceability back to baseline and architecture decisions

Validator entrypoint (current repo):
- `python custom_skills/impl-strategy/scripts/validate_task_graph.py`
- Wrapper: `./tools/run_impl_gate.sh`

## Scope
- Reads baseline handoff + arch-docs outputs (service inventory, decisions, contracts, ops expectations).
- Produces:
  - master implementation plan
  - phase plan with gates
  - machine-readable task graph
  - workstream partitioning / parallel execution plan (optional)
- Enforces: no task creation without upstream doc dependencies satisfied.

## Out of scope
- Writing architecture docs (arch-docs owns).
- Selecting cloud provider or changing baseline invariants (baseline owns).
- Executing implementation (coding/IaC). This skill outputs an execution plan.

## Inputs (hard dependencies)
Minimum required before starting impl-strategy:
- Baseline gate PASS
- `docs/baseline/BASELINE_HANDOFF.md`
- `docs/baseline/baseline_manifest.json`
- `docs/architecture/` exists and contains, at minimum:
  - service catalog / service inventory
  - Well-Architected pillar matrix
  - decision records for major choices (ADR/RFC), if any exist

## Outputs (mandatory)
Canonical repo locations:
- `docs/implementation/IMPLEMENTATION_STRATEGY.md` (master narrative plan)
- `docs/implementation/PHASE_PLAN.md` (phases + entry/exit gates)
- `docs/implementation/TASK_DAG.json` (machine-readable graph)
- `docs/implementation/TASK_CATALOG.md` (human-readable task list)
- Optional:
  - `docs/implementation/WORKTREE_PLAN.md` (parallelization)

## Determinism & Auditability Model
- Each task MUST have:
  - prerequisites (doc/decision dependencies)
  - inputs
  - outputs (artifacts changed)
  - validation step
  - acceptance criteria
- Each task MUST link to at least one upstream anchor:
  - baseline constraint / adherence requirement, OR
  - architecture element (service/catalog entry), OR
  - decision record (ADR/RFC)

Audit continuity:
- create run folder: `docs/audit/impl-strategy/<run-id>/`
- record:
  - `INPUT_SNAPSHOT.md` (paths + hashes if you add hashing later)
  - `QUALITY_GATE_REPORT.md`
  - `PHASE_COMPLETION_REPORT.md`
  - `OPEN_ITEMS.md`

Run-id convention:
`RUN-YYYYMMDD-HHMM-impl-strategy-<short-slug>`

## Known Current Repo Preconditions (you must satisfy to pass gates)
The current impl-strategy validator requires:
- baseline gate PASS
- `docs/implementation/` directory exists
- `custom_skills/impl-strategy/resources/policy/gate_definitions.yml` exists and is non-empty
