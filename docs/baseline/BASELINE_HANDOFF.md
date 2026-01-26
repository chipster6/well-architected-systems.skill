# Baseline Handoff Contract (arch-baseline → arch-docs)

This document is the deterministic interface between baseline and downstream architecture documentation. `arch-docs` MUST use this handoff as its authoritative input.

## 1) Handoff metadata
- Baseline ID:
- Provider: aws | azure | gcp
- Provider guidance review date (UTC):
- Toolchain applicability:
  - Kubernetes: yes | no
  - Terraform: yes | no
  - CDK: yes | no
- Handoff version:
- Owner:
- Generated on (UTC):

## 2) Preconditions (must already be true)
- Baseline gate status: PASS
- Baseline index: `docs/baseline/BASELINE_INDEX.md`
- Baseline manifest: `docs/baseline/baseline_manifest.json`
- Audit logs exist:
  - `docs/audit/evidence/evidence_log.jsonl`
  - `docs/audit/tool_calls/tool_call_audit.jsonl`

## 3) Canonical truth locations (arch-docs must not invent paths)
- Architecture output directory: `docs/architecture/`
- Audit output directory: `docs/audit/arch-docs/<run-id>/`
- Registries (read/write rules):
  - Read from `registries/` as canonical truth.
  - Update rules: arch-docs may expand service/event catalogs and contract/domain living docs, but must not rewrite baseline invariants without ADR.

## 4) Baseline invariants that arch-docs must respect
List the rules that arch-docs cannot violate.

### 4.1 Naming + IDs
- ADR numbering rule:
- RFC numbering rule:
- Service ID format:
- Contract ID format:
- Bounded context ID format:

### 4.2 Scope and boundaries
- In-scope:
- Out-of-scope:
- External dependencies:

### 4.3 Constraints (from constraints_registry)
- Regions policy:
- Data residency:
- Latency targets:
- Budget constraints:
- Stack constraints:

### 4.4 Security baseline (from SECURITY_BASELINE + security_controls_catalog)
- IAM baseline:
- Logging/audit baseline:
- Encryption/KMS baseline:
- Data classification baseline:

### 4.5 Operational baseline (from OPS_READINESS_STANDARD + slo_catalog)
- SLO/SLA intent:
- RTO/RPO intent:
- Runbook expectations:
- Incident response hooks:

## 5) Well-Architected governance contract (hard requirements)
`arch-docs` must comply with the pillar mappings defined here:
- `docs/baseline/WELL_ARCHITECTED_ADHERENCE_PLAN.md`

### 5.1 Pillar → required doc deliverables
For each pillar, list the minimum required doc types/sections arch-docs must produce and maintain.

| Pillar | Required doc types | Required sections (minimum) | Required evidence types | Review cadence |
|---|---|---|---|---|
|  |  |  |  |  |

### 5.2 Exception/waiver handling
- Any non-adherence must be documented as:
  - RFC (proposal) and ADR (decision), or a dedicated exception record
- Exceptions must include compensating controls and expiry/re-evaluation date.

## 6) arch-docs required doc inventory (by phase)
This is the deterministic doc plan arch-docs should execute.

### Phase D0 (scaffold + inventory)
- Required:
  - Architecture Overview entrypoint
  - Indexes (ADR log, RFC index, service catalog pointers)

### Phase D1 (RFC proposals)
- Required:
  - RFCs for major decisions:
    - service boundaries
    - data strategy
    - integration/eventing
    - security architecture decisions
    - ops architecture decisions

### Phase D2 (ADR lock)
- Required:
  - ADRs corresponding to accepted RFCs

### Phase D3 (service/security/ops expansion)
- Required:
  - Service specs for each container/service (as discovered)
  - Threat model docs (per boundary/service)
  - Runbooks (per service)

### Phase D4 (validation + audit bundle)
- Required:
  - Validation outputs
  - doc_manifest and audit bundle under `docs/audit/arch-docs/<run-id>/`

## 7) Required cross-links (enforced by validators)
Every downstream doc must link back to baseline anchors:

- Every RFC/ADR must reference:
  - `docs/baseline/BASELINE_INDEX.md`
  - `docs/baseline/WELL_ARCHITECTED_ADHERENCE_PLAN.md`
  - `registries/constraints_registry.yml`
  - security baseline and ops baseline docs (as applicable)

- Every Service Spec must reference:
  - service catalog entry (registries/service_catalog.yml)
  - bounded context ID (DOMAIN_MODEL baseline stub and/or living model)
  - contract IDs (CONTRACT_CATALOG baseline stub and/or living catalog)

- Every Threat Model must reference:
  - security controls catalog entries
  - relevant ADRs

- Every Runbook must reference:
  - SLO catalog entries
  - alerting/observability expectations

## 8) Evidence and audit requirements for arch-docs runs
- All external lookups performed during arch-docs must be recorded:
  - tool calls → `docs/audit/tool_calls/tool_call_audit.jsonl`
  - evidence items → `docs/audit/evidence/evidence_log.jsonl`
- All significant claims must have an evidence ID or a linked ADR.

## 9) Open items handed off to arch-docs
If any open items remain, list them as actionable, phase-targeted items.

| Open item ID | Description | Target phase | Owner | Blocking? (Y/N) |
|---|---|---|---|---|
|  |  |  |  |  |

## 10) Acceptance criteria: “arch-docs can start”
- Baseline gate PASS
- All baseline invariants documented above
- Well-Architected plan complete and mapped
- Registries exist and contain minimum required fields
- Audit structure exists and is writable
