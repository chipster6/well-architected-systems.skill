---
name: cloudrail-arch-docs
description: Deterministic, contract-first workflow for producing CloudRail architecture documentation with MCP evidence and Well-Architected coverage.
---

# CloudRail Architecture Documentation Skill (v2)

## Purpose
Provide CloudRail-specific architecture and documentation guidance for the Control Plane and Tenant Plane with evidence-by-construction, schema-first contracts, enforced MCP validation, and deterministic token replacement gates.

## Allowed and Forbidden Targets (Defaults)
- Allowed by default: `docs/**`, `contracts/schemas/**`, `contracts/examples/**`
- Forbidden unless explicitly requested: `scripts/**` (including `./scripts/docs_verify.sh`, `./scripts/validate_schemas.sh`), `infra/**`, `services/**`, `runners/**`, any file deletions or moves

## Hard Gates (Non-Negotiable)
- MUST use CloudRail terminology: Control Plane, Tenant Plane, AssumeRole with external ID, permission boundaries, Step Functions orchestrator, hardened runners, evidence-by-construction, schema-first contracts.
- MUST follow Canada-first defaults with `ca-central-1` unless a contract explicitly allows another region.
- MUST enforce contract-first rules: any DM doc that references `contracts/schemas/*.schema.json` requires the schema and required examples under `contracts/examples/**` to exist already or be created in the same patch.
- Validation scripts are required **only when docs/** or **contracts/** are modified during a doc-generation run. When required, run and paste PASS outputs for both:
  - `./scripts/docs_verify.sh`
  - `./scripts/validate_schemas.sh`
- MUST NOT edit `./scripts/docs_verify.sh` or `./scripts/validate_schemas.sh` unless explicitly requested by the user.
- MUST NOT delete or move files unless explicitly requested; drift cleanup defaults to deprecation stubs with canonical pointers.
- MUST avoid banned tokens and placeholders in produced docs: no angle-bracket placeholders and no placeholder stubs. Templates may use `TOKEN_*`, final docs may not (see TOKEN_REPLACEMENT_GATE).
- MUST treat AI output as draft input; deterministic systems execute changes.
- MUST NOT use HTML line breaks in Mermaid labels; use newline escapes or restructure the diagram.
- MCP Preflight/Postflight gates are mandatory for normative claims (see references below).

## Stop Conditions
If any of the following occur, output `BLOCKER` with the exact missing files or violated rule and stop:
- A DM doc references a schema missing from `contracts/schemas/` and the schema is not included in the same patch.
- Required examples under `contracts/examples/` are missing for any new schema.
- `./scripts/docs_verify.sh` or `./scripts/validate_schemas.sh` fails or does not return PASS when they are required to run.
- Any delete or move is attempted without explicit user request.
- Any edits to `./scripts/docs_verify.sh` or `./scripts/validate_schemas.sh` are attempted without explicit user request.
- Any edits outside the allowed targets are attempted without explicit user request.
- Required MCP tools cannot be executed for normative claims and the section cannot be marked `UNVERIFIED EXTERNALLY`.

## Required Output Contract
Before edits, provide a `PATCH_PLAN_BY_FILEPATH` section. After edits, provide:
- `DIFFS`: unified diffs grouped by file path.
- `VALIDATION_OUTPUT`: PASS output for `./scripts/docs_verify.sh` and `./scripts/validate_schemas.sh` (only when docs/** or contracts/** changed in the run).
- `MCP_EVIDENCE_LOG.md`: populated with preflight/postflight calls for normative claims; each entry must include `evidence_id` formatted `MCP-YYYYMMDD-NNNN`.
- `WELL_ARCHITECTED_PILLAR_MATRIX.md`: completed for architecture decisions.
- `PHASE_COMPLETION_REPORT_PN.md`: one per completed phase (0–6), e.g., `PHASE_COMPLETION_REPORT_P0.md` … `PHASE_COMPLETION_REPORT_P6.md`.

## Core Workflow
- Read `AGENTS.md` and confirm governance rules.
- Read `references/mcp-validation.md` for required MCP calls and timing.
- Read `references/reference-policy.md` for minimum references and claim rules.
- Read `docs/09_GOVERNANCE/GOV-ARCH-001-Architecture-Documentation-Index.md`.
- Read `docs/03_CONTRACTS/REGISTRY.md` for contract ownership and schema expectations.
- Use `references/document-selection.md` to choose the document type.
- Use templates under `templates/` (see `references/templates.md` pointer) to apply the correct template.
- Follow `references/workflow.md` for sequencing and validation.

## Workflow Entry Points
- `AGENTS.md`
- `references/mcp-validation.md`
- `references/reference-policy.md`
- `references/document-selection.md`
- `references/templates.md` (pointer to `templates/`)
- `references/workflow.md`

## Canonical CloudRail Doc Families
- `docs/02_ARCHITECTURE/ARC-*.md`
- `docs/03_CONTRACTS/DM-*.md` and `docs/03_CONTRACTS/REGISTRY.md`
- `contracts/schemas/*.schema.json` and `contracts/examples/**`
- `docs/04_SERVICES/SERVICE_*.md`
- `docs/05_WORKFLOWS/WORKFLOW_*.md` and `docs/05_WORKFLOWS/RUNNER_CONTRACT.md`
- `docs/07_OPERATIONS/*.md`
- `docs/09_GOVERNANCE/GOV-ARCH-001-Architecture-Documentation-Index.md` (update when adding ARC, DM, service, or workflow docs)

## Phase Model (v2)
- Phase 0: Intake & Governance — read AGENTS/reference files, confirm targets, classify claims; start MCP Preflight calls.
- Phase 1: Decision Inputs — gather ADRs/constraints; update MCP_EVIDENCE_LOG preflight entries.
- Phase 2: Drafting — apply templates; ensure schema-first for DM; maintain WELL_ARCHITECTED_PILLAR_MATRIX.
- Phase 3: Validation — run MCP Postflight checks; update evidence log; mark unverifiable sections.
- Phase 4: Quality Gates — apply `references/quality-gates.md`; ensure structure/contract/consistency/MCP/WA gates pass.
- Phase 5: Script Validation — run `./scripts/docs_verify.sh` and `./scripts/validate_schemas.sh` only when docs/** or contracts/** changed.
- Phase 6: Completion — produce `PHASE_COMPLETION_REPORT_PN.md` (e.g., `PHASE_COMPLETION_REPORT_P6.md`), diffs, validation outputs (when docs/contracts changed), and update governance indexes.
