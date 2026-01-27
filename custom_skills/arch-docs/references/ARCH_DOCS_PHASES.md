# arch-docs — Phased Workflow and Gates

This workflow defines arch-docs as a deterministic pipeline. Each phase produces mandatory artifacts and must pass gates before proceeding.

## Global invariants
1) Do not proceed if baseline gate is not PASS.
2) All normative claims must have evidence or be explicitly `UNVERIFIED EXTERNALLY`.
3) No file moves/deletes unless explicitly requested.
4) Contract-first: if a doc references a schema/contract, the schema + an example MUST be created/updated in the same patch.
5) Progressive disclosure: SKILL.md remains concise; this file is the long-form runbook.

## Required inputs (must exist before D0)
- Baseline:
  - `docs/baseline/BASELINE_INDEX.md`
  - `docs/baseline/BASELINE_HANDOFF.md`
  - `docs/baseline/baseline_manifest.json`
  - `docs/baseline/WELL_ARCHITECTED_ADHERENCE_PLAN.md`
- Registries:
  - `registries/constraints_registry.yml`
  - `registries/security_controls_catalog.yml`
  - `registries/slo_catalog.yml`
- Audit substrate:
  - `docs/audit/evidence/evidence_log.jsonl`
  - `docs/audit/tool_calls/tool_call_audit.jsonl`
- Arch-docs policy inputs (must be non-empty to pass current validator):
  - `custom_skills/arch-docs/resources/policy/required_sections.yml`
  - `custom_skills/arch-docs/resources/policy/crosslink_rules.yml`
  - `custom_skills/arch-docs/resources/policy/placeholder_rules.yml`

## Phase D0 — Preflight and Inventory
### Objective
Establish the doc inventory, targets, and claim classification before drafting.

### Entry gate D0-E
- Baseline gate PASS (`./tools/run_baseline_gate.sh`)
- Required inputs present (see above)
- Run folder created: `docs/audit/arch-docs/<run-id>/`

### Mandatory outputs
- `docs/audit/arch-docs/<run-id>/DOC_INVENTORY.md`
- `docs/audit/arch-docs/<run-id>/CLAIM_CLASSIFICATION.md`
- `docs/audit/arch-docs/<run-id>/PATCH_PLAN_BY_FILEPATH.md`

### Exit gate D0-X
- Inventory lists required doc families derived from baseline adherence plan
- Claim classification explicitly marks normative sections requiring evidence
- Patch plan enumerates every file to create/edit (no implicit files)

---

## Phase D1 — Decision Proposals (RFCs) as Needed
### Objective
Create RFC proposals for unresolved major architecture decisions required to write coherent docs.

### Entry gate D1-E
- D0-X passed

### Mandatory outputs (as applicable)
- `docs/decisions/RFC-<id>.md`
- Update `docs/decisions/RFC_INDEX.md` (if you maintain indexes)

### Exit gate D1-X
- Each RFC includes: context, options, tradeoffs, risks, recommendation, and links back to baseline constraints + adherence plan
- Normative claims inside RFCs have evidence plan entries (even if evidence is acquired later)

---

## Phase D2 — Decision Lock (ADRs)
### Objective
Convert accepted RFC recommendations into ADRs for traceability.

### Entry gate D2-E
- D1-X passed OR “no RFCs required” recorded in the run folder

### Mandatory outputs
- `docs/decisions/ADR-<id>.md`
- `docs/decisions/ADR_INDEX.md` updated (if used)

### Exit gate D2-X
- ADRs reference baseline anchors (index + adherence plan) and constraints registry
- ADRs include explicit consequences and follow-ups

---

## Phase D3 — Drafting and Expansion (Architecture / Services / Security / Ops / Contracts)
### Objective
Produce the actual architecture documentation set.

### Entry gate D3-E
- D2-X passed
- `docs/architecture/` exists

### Mandatory outputs (minimum set for first pass)
- `docs/architecture/ARC_OVERVIEW.md`
- `docs/architecture/C4_Component.md` (baseline already includes Context/Container)
- `docs/architecture/SERVICE_CATALOG.md` (service/container inventory)
- `docs/architecture/SECURITY_ARCHITECTURE.md`
- `docs/architecture/THREAT_MODEL.md`
- `docs/architecture/OPERATIONS_MODEL.md`
- `docs/architecture/WELL_ARCHITECTED_PILLAR_MATRIX.md` (provider-specific pillar set from baseline)

### Conditional outputs
If the system exposes contracts:
- `docs/contracts/` family + `contracts/schemas/` + `contracts/examples/`

### Exit gate D3-X
- Every doc cross-links to baseline anchors (index + adherence plan) and relevant ADR/RFC
- Naming consistency: service IDs and boundaries match catalog/registries
- No placeholder markers remain in mandatory sections (per placeholder policy)

---

## Phase D4 — Evidence Postflight and Normalization
### Objective
Validate normative claims and normalize findings into registries/docs.

### Entry gate D4-E
- D3-X passed

### Mandatory outputs
- Append tool calls: `docs/audit/tool_calls/tool_call_audit.jsonl`
- Append evidence: `docs/audit/evidence/evidence_log.jsonl`
- Update rollup: `docs/audit/EVIDENCE_LOG.md`
- `docs/audit/arch-docs/<run-id>/EVIDENCE_SUMMARY.md`

### Exit gate D4-X
- Every normative claim links to an evidence_id OR is explicitly `UNVERIFIED EXTERNALLY`
- Evidence entries include normalization targets (doc path + section, or registry path + field)

---

## Phase D5 — Quality Gates (structure, crosslinks, Well-Architected coverage)
### Objective
Run deterministic checks to ensure coherence and completeness.

### Entry gate D5-E
- D4-X passed

### Mandatory outputs
- `docs/audit/arch-docs/<run-id>/QUALITY_GATE_REPORT.md`

### Exit gate D5-X (fail closed)
- Required sections satisfied per doc type policy
- Crosslink rules satisfied (baseline anchors + decision links)
- Well-Architected pillar matrix complete for all decision areas created/modified in this run
- Contract-first completeness satisfied where applicable

---

## Phase D6 — Publication and Handoff
### Objective
Publish arch-docs output and produce a clean handoff for impl-strategy.

### Entry gate D6-E
- D5-X passed
- Current repo validator passes: `./tools/run_arch_docs_gate.sh`

### Mandatory outputs
- `docs/audit/arch-docs/<run-id>/PHASE_COMPLETION_REPORT.md`
- `docs/audit/arch-docs/<run-id>/OPEN_ITEMS.md`
- Update architecture index files if used (e.g., `docs/architecture/ARCHITECTURE_INDEX.md`)

### Exit gate D6-X
- arch-docs gate PASS
- Handoff explicitly calls out:
  - service catalog
  - contract inventory (if any)
  - decisions created/modified
  - evidence ids created/modified
  - any open items and their owners
