# Project Instructions — well-architected-systems.skill

## Purpose
This repository defines a three-skill bundle for producing Well-Architected, auditable architecture documentation and an implementation strategy:
1) `arch-baseline`: establish canonical scope, provider selection, invariants, and governance contracts.
2) `arch-docs`: expand baseline into a complete architecture documentation set with evidence and deterministic gates.
3) `impl-strategy`: convert baseline + architecture docs into an executable implementation strategy and dependency DAG.

The bundle is multi-cloud capable: AWS, Azure, and GCP are supported. Baseline selects the provider and the applicable Well-Architected framework for the system.

## Repository Structure (canonical)
- Skills live under `custom_skills/<skill-name>/`
  - `SKILL.md` is the entry point for that skill.
  - `references/` contains long-form workflows, gates, checklists.
  - `resources/` contains templates, schemas, examples.
  - `scripts/` contains deterministic validators and scaffolding utilities.
- Project docs live under `docs/`
  - Baseline docs: `docs/baseline/`
  - Architecture docs: `docs/architecture/`
  - Implementation strategy: `docs/implementation/`
  - Audit logs: `docs/audit/`

Do not introduce parallel competing doc roots. If older drafts exist under `project-scope/`, treat them as non-canonical unless explicitly promoted.

## Skill Authoring Standards (hard rules)
### SKILL.md frontmatter
Each `custom_skills/*/SKILL.md` MUST start with YAML frontmatter including:
- `name`: lowercase, hyphenated, <= 64 chars
- `description`: includes explicit triggers and “when to use”
Keep the description “discovery-grade”: it must cause correct selection in a skill router. :contentReference[oaicite:1]{index=1}

### Progressive disclosure
- Keep `SKILL.md` body concise and procedural.
- Put the full phased workflows and detailed gates in `references/`.
- Scripts and templates are loaded only when needed. :contentReference[oaicite:2]{index=2}

### Determinism policy
Prefer instructions over scripts. Use scripts only for:
- deterministic validation (fail closed),
- normalization transforms,
- repeatable scaffolding. :contentReference[oaicite:3]{index=3}

## Global Invariants (apply to all three skills)
1) Baseline-first: `arch-docs` and `impl-strategy` must not proceed if the baseline gate is failing.
2) Fail closed: if a required input is missing, stop and produce a concrete remediation list.
3) Canonical paths only: downstream skills must not invent new “truth locations” for baseline artifacts.
4) Traceability: every normative requirement must be tied to one of:
   - provider framework source (captured as evidence), or
   - a decision record (ADR/RFC) that justifies deviation.
5) No silent drift: any change to baseline invariants requires an ADR and must update the baseline handoff.

## Auditability Model (required)
### Logs
All skills must append to:
- `docs/audit/tool_calls/tool_call_audit.jsonl`
- `docs/audit/evidence/evidence_log.jsonl`

Additionally maintain human rollups:
- `docs/audit/EVIDENCE_LOG.md`
- `docs/audit/tool_calls/TOOL_CALL_AUDIT_SUMMARY.md`

### Evidence requirements
For any normative claim (MUST/SHALL/REQUIRED):
- create or reference an Evidence ID and record:
  - source type (official docs, standard, whitepaper),
  - retrieval date,
  - extracted rule,
  - normalization target (registry/doc path + section),
  - related ADR/RFC if applicable.

If external validation cannot be performed, label the claim:
`UNVERIFIED EXTERNALLY` + reason + follow-up plan.

## Multi-Cloud Well-Architected Framework Handling
Baseline selects the provider framework and pillar set.

Canonical pillar sets (for reference):
- AWS Well-Architected is built around six pillars, including Sustainability. :contentReference[oaicite:4]{index=4}
- Azure Well-Architected is organized around five pillars. :contentReference[oaicite:5]{index=5}
- Google Cloud’s architecture framework pillars include Operational Excellence, Security/Privacy/Compliance, Reliability, Cost Optimization, and Performance Optimization. :contentReference[oaicite:6]{index=6}

Rule:
- The repo must store the selected provider framework in `docs/baseline/WELL_ARCHITECTED_ADHERENCE_PLAN.md`.
- The pillar table in that plan must match the selected provider’s pillar set.
- Any “provider-agnostic requirement” must be explicitly marked as such and must not contradict the selected provider framework.

## Gates (CI and local)
### Baseline Gate (must PASS first)
- CI: `.github/workflows/baseline-gate.yml`
- Local: `./tools/run_baseline_gate.sh`

Baseline must ensure:
- Required baseline docs exist under `docs/baseline/`
- `docs/baseline/WELL_ARCHITECTED_ADHERENCE_PLAN.md` is structurally valid
- Registries exist and are non-empty:
  - `registries/constraints_registry.yml`
  - `registries/security_controls_catalog.yml`
  - `registries/slo_catalog.yml`

### Architecture Docs Gate
- CI: `.github/workflows/arch-docs-gate.yml`
- Local: `./tools/run_arch_docs_gate.sh`

Arch-docs must ensure, at minimum:
- `docs/architecture/` exists
- An architecture doc inventory exists for the run under `docs/audit/arch-docs/<run-id>/`
- Cross-links exist back to baseline anchors (baseline index, adherence plan, registries)
- Evidence links exist for normative sections or are explicitly marked unverified

### Implementation Strategy Gate
- CI: `.github/workflows/impl-strategy-gate.yml`
- Local: `./tools/run_impl_gate.sh`

Impl-strategy must ensure, at minimum:
- `docs/implementation/` exists
- `docs/implementation/TASK_DAG.json` exists, is valid JSON, and is acyclic
- Every task includes:
  - prerequisites (doc/decision dependencies),
  - outputs,
  - validation step,
  - acceptance criteria
- Worktree or parallelization plan is defined if used.

## Required Run Artifacts (per skill run)
Every skill execution produces a run folder:
- `docs/audit/<skill>/<run-id>/PHASE_COMPLETION_REPORT.md`
- `docs/audit/<skill>/<run-id>/FILES_CHANGED.md`
- `docs/audit/<skill>/<run-id>/OPEN_ITEMS.md`
- `docs/audit/<skill>/<run-id>/QUALITY_GATE_REPORT.md` (when applicable)

Run ID format (deterministic):
`RUN-YYYYMMDD-HHMM-<short-slug>`

## Output Contract for Agents (how patches must be proposed)
When making changes, always produce:
1) `PATCH_PLAN_BY_FILEPATH` listing creates/edits.
2) A short “why” per file (one sentence).
3) Gate impact: which gate(s) should be re-run.
4) Acceptance criteria for the patch.

Do not introduce placeholders that would let gates pass without real content.

## Scope control
- `arch-baseline` owns:
  - provider selection,
  - scope boundaries,
  - baseline invariants,
  - well-architected adherence plan,
  - baseline manifest.
- `arch-docs` owns:
  - architecture documentation expansion,
  - service/workflow/contract specs,
  - evidence capture and normalization.
- `impl-strategy` owns:
  - task DAG + phases + milestones,
  - dependency mapping to docs/decisions,
  - parallelization/worktree plan.

Downstream skills must not rewrite baseline invariants without ADR + handoff update.
