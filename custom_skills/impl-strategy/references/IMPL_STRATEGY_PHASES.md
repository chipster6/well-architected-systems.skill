# impl-strategy — Phased Workflow and Gates

This workflow defines impl-strategy as a deterministic planning pipeline. Each phase produces mandatory artifacts and must pass gates before proceeding.

## Global invariants
1) Do not proceed if baseline gate is not PASS.
2) Do not create tasks that are not traceable to baseline/architecture/decisions.
3) Fail closed if required policy files are missing/empty.
4) Prefer reversible sequencing: plan for incremental delivery, verification, and rollback where applicable.
5) Progressive disclosure: this file is the long-form runbook; keep SKILL.md concise.

## Required inputs (must exist before I0)
- Baseline:
  - `docs/baseline/BASELINE_HANDOFF.md`
  - `docs/baseline/baseline_manifest.json`
  - `docs/baseline/WELL_ARCHITECTED_ADHERENCE_PLAN.md`
- Architecture docs:
  - `docs/architecture/` exists
  - service inventory exists (recommended: `docs/architecture/SERVICE_CATALOG.md`)
  - decisions exist where major choices were made (`docs/decisions/ADR-*.md`, optional but recommended)
- Impl-strategy policy inputs (must be non-empty):
  - `custom_skills/impl-strategy/resources/policy/gate_definitions.yml`
  - `custom_skills/impl-strategy/resources/policy/dependency_rules.yml`
  - `custom_skills/impl-strategy/resources/policy/labeling_rules.yml`
  - `custom_skills/impl-strategy/resources/policy/parallelization_heuristics.yml`

## Phase I0 — Preflight (readiness snapshot)
### Objective
Freeze the planning inputs for this run and confirm readiness.

### Entry gate I0-E
- Baseline gate PASS (`./tools/run_baseline_gate.sh`)
- Required inputs present (see above)
- Run folder created: `docs/audit/impl-strategy/<run-id>/`

### Mandatory outputs
- `docs/audit/impl-strategy/<run-id>/INPUT_SNAPSHOT.md`
- `docs/audit/impl-strategy/<run-id>/PATCH_PLAN_BY_FILEPATH.md`

### Exit gate I0-X
- Input set is explicitly enumerated (no implicit dependencies)
- Any missing architecture prerequisites are listed in `OPEN_ITEMS.md` and the run stops

---

## Phase I1 — Decomposition into Epics (workstreams)
### Objective
Derive top-level workstreams from the architecture and baseline constraints.

### Entry gate I1-E
- I0-X passed

### Mandatory outputs
- `docs/implementation/EPICS.md` (workstreams with owners/roles)

### Exit gate I1-X
- Each epic references:
  - at least one architecture anchor (service/catalog), and
  - at least one baseline anchor (constraint or adherence requirement)

---

## Phase I2 — Task DAG generation (stories/tasks/subtasks)
### Objective
Create the machine-readable dependency graph and a readable catalog.

### Entry gate I2-E
- I1-X passed

### Mandatory outputs
- `docs/implementation/TASK_DAG.json`
- `docs/implementation/TASK_CATALOG.md`

### Exit gate I2-X (fail closed)
- DAG is acyclic
- Every node has:
  - id, title, owner_role
  - prerequisites (ids)
  - inputs (artifact refs)
  - outputs (artifact refs)
  - validation step
  - acceptance criteria
- Every node references at least one upstream anchor:
  - baseline/architecture/decision link

---

## Phase I3 — Phase plan (milestones + gates)
### Objective
Group tasks into delivery phases that can be executed incrementally.

### Entry gate I3-E
- I2-X passed

### Mandatory outputs
- `docs/implementation/PHASE_PLAN.md`

### Exit gate I3-X
- Each phase has:
  - entry gate (prereqs)
  - exit gate (verification criteria)
  - deliverable artifacts
  - rollback/containment notes for irreversible steps

---

## Phase I4 — Parallelization plan (optional)
### Objective
Define how work can proceed in parallel without conflicts.

### Entry gate I4-E
- I3-X passed

### Mandatory outputs (if parallelizing)
- `docs/implementation/WORKTREE_PLAN.md`

### Exit gate I4-X
- Each workstream has bounded file ownership (no overlapping write sets)
- Merge sequencing and validation gates are explicit

---

## Phase I5 — Quality gates and validation
### Objective
Ensure the strategy is coherent, governed, and executable.

### Entry gate I5-E
- I3-X passed (and I4-X if parallelization is used)

### Mandatory outputs
- `docs/audit/impl-strategy/<run-id>/QUALITY_GATE_REPORT.md`

### Exit gate I5-X (fail closed)
- No tasks violate baseline constraints
- All tasks map to at least one verification mechanism
- No “implementation” tasks exist without upstream design decision references when decisions are required

---

## Phase I6 — Publication and handoff to execution
### Objective
Publish strategy artifacts and ensure repo gates pass.

### Entry gate I6-E
- I5-X passed
- Current repo validator passes: `./tools/run_impl_gate.sh`

### Mandatory outputs
- `docs/implementation/IMPLEMENTATION_STRATEGY.md`
- `docs/audit/impl-strategy/<run-id>/PHASE_COMPLETION_REPORT.md`
- `docs/audit/impl-strategy/<run-id>/OPEN_ITEMS.md`

### Exit gate I6-X
- impl-strategy gate PASS
- Strategy includes:
  - critical path
  - risks + mitigations for high-blast-radius tasks
  - verification checkpoints per phase
