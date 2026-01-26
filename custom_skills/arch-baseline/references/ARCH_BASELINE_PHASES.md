# arch-baseline — Phased Artifact Workflow and Gates

This document defines the baseline workflow as a deterministic pipeline. Each phase produces mandatory artifacts and must pass gates before proceeding.

## Global rule
All external lookups (MCP/web) must produce:
1. a tool-call audit record (`docs/audit/tool_calls/tool_call_audit.jsonl`)
2. an evidence record (`docs/audit/evidence/evidence_log.jsonl` and/or `docs/audit/EVIDENCE_LOG.md`)
3. normalization into a registry/policy or a baseline doc section

---

## Phase B0 — Documentation Governance, Standards, Canonicalization

### Objective
Lock documentation governance and “where truth lives” before any provider specifics.

### Mandatory artifacts
- `docs/baseline/DOCS_GOVERNANCE.md`
- `docs/baseline/ADR_POLICY.md`
- `docs/baseline/golden_templates/` (directory exists)
- `docs/audit/EVIDENCE_LOG.md`
- `docs/audit/tool_calls/tool_call_audit.jsonl`
- Registries initialized:
  - `registries/constraints_registry.yml`
  - `registries/security_controls_catalog.yml`
  - `registries/slo_catalog.yml`

### Quality / dependency gate B0
Pass only if:
- Output locations are defined in governance (docs paths, registry paths, audit paths)
- Naming + ID conventions exist (ADR/RFC numbering, service IDs, contract IDs, bounded context IDs)
- Evidence + tool-call audit files exist (even if empty at this point)
- Registries exist (may be empty but must be real files)

---

## Phase B1 — System Definition (What the system is)

### Objective
Define scope and high-level intent; constrain scope creep.

### Mandatory artifacts
- `docs/baseline/SYSTEM_CHARTER.md`
- `docs/baseline/SCOPE_BOUNDARIES.md`

### Quality / dependency gate B1
Pass only if:
- Goals/non-goals and success criteria are specified
- Explicit in-scope/out-of-scope boundaries exist
- External dependencies and assumptions are stated
- The charter and scope are referenced by governance (or linked from BASELINE_INDEX once created)

---

## Phase B2 — Cloud Provider Evaluation and Decision (RFC → ADR)

### Objective
Select provider with explicit criteria and lock it as a decision.

### Mandatory artifacts
- `docs/baseline/PROVIDER_COMPARISON_RFC.md`
- `docs/baseline/CLOUD_PROVIDER_DECISION_ADR.md`

### Quality / dependency gate B2
Pass only if:
- ADR references the RFC
- Decision includes evaluation criteria and rationale
- Constraints registry is updated with any provider-driven constraints (regions, residency, compliance, etc.)

---

## Phase B3 — Provider Pack Activation and Toolchain Applicability

### Objective
Activate the chosen provider pack and decide applicability of Kubernetes/Terraform/CDK research tracks.

### Mandatory artifacts
- `docs/baseline/TOOLCHAIN_BASELINE.md` (declares IaC and runtime choices, even if only “selected approach”)
- Provider pack selection recorded (can be within ADR or TOOLCHAIN_BASELINE)
- Registries updated with baseline structural constraints from provider pack:
  - account/subscription/project model
  - region policy
  - network baseline intent (even if minimal)

### Gate B3
Pass only if:
- Provider pack is selected and its pillar set is known
- Toolchain applicability is explicit (Kubernetes yes/no; Terraform yes/no; CDK yes/no)
- Registries contain at least provider structural constraints (non-empty where applicable)

---

## Phase B4 — Well-Architected Adherence Plan (Governing Contract)

### Objective
Produce the governing plan that downstream `arch-docs` must adhere to.

### Mandatory artifacts
- `docs/baseline/WELL_ARCHITECTED_ADHERENCE_PLAN.md`

### Mandatory content requirements
- Provider selected and named
- Complete pillar set included
- For every pillar:
  - required doc types/sections for downstream `arch-docs`
  - required evidence types
  - review cadence and exception/waiver rules
- Internal consistency:
  - no conflicts with constraints/security/ops registries

### Gate B4
Pass only if:
- All pillars are present
- Each pillar maps to at least one downstream deliverable and one evidence type
- Exception/waiver process is defined
- Evidence references exist for the pillar set and key baseline practices

---

## Phase B5 — Post-Decision Research + Evidence Capture + Normalization

### Objective
Collect authoritative, up-to-date guidance via MCP/web and normalize into registries/policies.

### Mandatory artifacts
- Tool-call audit trail updated:
  - `docs/audit/tool_calls/tool_call_audit.jsonl`
- Evidence log updated:
  - `docs/audit/evidence/evidence_log.jsonl`
  - `docs/audit/EVIDENCE_LOG.md` (human rollup)
- Normalized registry updates (must be non-empty in relevant areas):
  - `registries/constraints_registry.yml`
  - `registries/security_controls_catalog.yml`
  - `registries/slo_catalog.yml`

### Gate B5
Pass only if:
- Each research topic produces at least one evidence record and one normalization target
- Failed tool calls are recorded with error details
- For chosen provider: Well-Architected pillar sources are consulted and recorded
- For selected toolchain: Kubernetes/Terraform/CDK sources are consulted and recorded (only if applicable)

---

## Phase B6 — Baseline Architecture Snapshot + Domain/Contract Initialization

### Objective
Provide enough architectural shape for `arch-docs` to expand without re-asking foundational questions.

### Mandatory artifacts
- `docs/baseline/C4_Context.md`
- `docs/baseline/C4_Container.md`
- `docs/baseline/DOMAIN_MODEL.md` (initialized stub)
- `docs/baseline/CONTRACT_CATALOG.md` (initialized stub)

### Gate B6
Pass only if:
- C4 Context and Container exist and use canonical naming/IDs
- Domain model stub includes bounded contexts list + glossary + integration style notes
- Contract catalog stub includes naming/versioning rules + ownership model + catalog index structure
- Ownership rule stated: baseline initializes; arch-docs expands and maintains living versions

---

## Phase B7 — Security & Ops Baselines + Handoff Contract + Baseline Publication Gate

### Objective
Finalize security/ops baseline and produce deterministic handoff to downstream skill.

### Mandatory artifacts
- `docs/baseline/SECURITY_BASELINE.md`
- `docs/baseline/OPS_READINESS_STANDARD.md`
- `docs/baseline/BASELINE_INDEX.md`
- `docs/baseline/BASELINE_HANDOFF.md`
- `docs/baseline/baseline_manifest.json`

### Gate B7 (Baseline Publication Gate)
Pass only if:
- Security baseline covers identity, logging/audit, encryption/key management, data classification rules
- Ops baseline covers SLO intent, incident hooks, RTO/RPO targets (if applicable), runbook expectations
- BASELINE_INDEX links all baseline artifacts and registries
- BASELINE_HANDOFF specifies:
  - required `arch-docs` doc inventory by phase
  - required cross-links back to baseline
  - required registries and minimum fields
  - evidence expectations and locations
- baseline_manifest.json lists all baseline artifacts and their required status

On pass: downstream skills may proceed.
On fail: stop. Resolve gaps, update evidence and registries, re-run validation.
