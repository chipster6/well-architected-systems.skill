---
doc_id: WELLARCH-BASE-001
doc_type: well_architected_adherence_plan
status: draft
phase: baseline
provider: unselected
framework_name: Well-Architected Framework (selected post-decision)
framework_version: selected post-decision
owner: architecture-working-group
review_cadence: monthly
last_reviewed: 2026-01-20
next_review_due: 2026-02-20
related_docs:
  - docs/baseline/SYSTEM_CHARTER.md
  - docs/baseline/C4_Context.md
  - docs/baseline/C4_Container.md
  - docs/baseline/PROVIDER_COMPARISON_RFC.md
  - docs/baseline/CLOUD_PROVIDER_DECISION_ADR.md
evidence_log: docs/audit/EVIDENCE_LOG.md
---

# Well-Architected Adherence Plan

## 1. Purpose
Define how this repository’s baseline produces Well-Architected-governed documentation regardless of which provider is selected (AWS/Azure/GCP). Provider-specific pillar mapping is materialized after the provider decision using provider packs.

## 2. Provider Selection Procedure
This repository treats provider selection as a first-class decision. The baseline workflow is:
1. Create/maintain the provider comparison RFC: `docs/baseline/PROVIDER_COMPARISON_RFC.md`
2. Decide and record the selected provider in an ADR: `docs/baseline/CLOUD_PROVIDER_DECISION_ADR.md`
3. Materialize provider-specific Well-Architected mapping from the chosen provider pack (see section 3).

## 3. Provider Packs
Provider packs are the canonical location for provider-specific pillar sets, required doc families, and evidence expectations:
- AWS: `custom_skills/arch-baseline/resources/provider_packs/aws/`
- Azure: `custom_skills/arch-baseline/resources/provider_packs/azure/`
- GCP: `custom_skills/arch-baseline/resources/provider_packs/gcp/`

Each pack must contain, at minimum:
- pillar definitions (canonical names)
- required doc families per provider
- control mappings / evidence expectations per provider

## 4. Materializing Pillar Mapping Post-Decision
When the provider decision ADR is Accepted, the baseline process must:
- set `provider` in this document to the selected provider (`aws`, `azure`, or `gcp`)
- set `framework_name` and `framework_version` to the selected framework
- replace this template-mode section 4 with a provider-specific “Pillar-to-Documentation Mapping” table sourced from the chosen provider pack
- ensure every normative requirement is traceable to evidence or an ADR/RFC exception process

This keeps the repo provider-neutral while still producing deterministic, provider-specific outputs during real project runs.

## 5. Baseline Requirements (Provider-Agnostic)
These requirements apply regardless of provider. If compliance is not possible, an exception must be logged.

### 5.1 Security Baseline
- Enforce least-privilege access controls and audit access changes.
- Encrypt sensitive data at rest and in transit using provider-approved mechanisms.
- Maintain security-relevant logs with retention aligned to organizational requirements.
- Apply data classification labels and restrict sensitive data movement across trust boundaries.

### 5.2 Reliability Baseline
- Publish SLO targets per service; document RTO/RPO values for shared data stores.
- Run weekly backup integrity checks and quarterly failover exercises.
- Model failure modes (network isolation, AZ outage) and document mitigations.

### 5.3 Operational Excellence Baseline
- Define production readiness checklist for every deployable unit.
- Maintain runbooks for paging, manual overrides, and GTM escalation.
- Implement incident response hooks with on-call rotation coverage.

## 6. Review Procedure
Describe how well-architected reviews are executed and how artifacts are captured.

### 6.1 Review Events
- **Baseline review:** triggered when baseline artifacts are first approved.
- **Milestone review:** executed at each quarterly release gate.
- **Pre-production review:** executed before enabling a new production environment, region, or major workload.

### 6.2 Review Output Artifacts
- Summary of findings, categorized by pillar risk.
- Remediation backlog prioritized by severity.
- Evidence log entries referencing IaC commits or config snapshots.
- ADRs for structural changes or exception approvals.

## 7. Evidence and Audit Rules
### 7.1 Evidence ID Format
- Evidence IDs follow: `EVD-YYYYMMDD-NNNN` (example: `EVD-20260126-0001`).

### 7.2 Evidence Locations
- Evidence log: `docs/audit/EVIDENCE_LOG.md`
- IaC references: `iac/terraform/`
- Config snapshots: `artifacts/config-snapshots/`
- Test results: `artifacts/test-results/`

### 7.3 Traceability Requirements
Every pillar row must reference at least one architecture doc section and one evidence artifact (or planned evidence with due date) to satisfy the baseline gate.

## 8. Exception / Waiver Process
- Submit RFC detailing rationale, blast radius, and compensating controls.
- Record decision via ADR with expiry/review date.
- Track exception in the evidence log until retired.

## 9. Acceptance Criteria (Baseline Gate)
Baseline is green only when:
- Provider/framework metadata is populated with concrete values.
- Provider selection procedure and provider pack references are present in template-mode.
- After provider selection, pillar mapping is materialized from the chosen provider pack with owners/cadences.
- Evidence storage locations exist and are accessible.
- Exception workflow is documented and linked to ADRs.
- Related baseline documents exist and link to this plan.

## 10. Change Log
| Date | Change | Author | Reference (ADR/RFC) |
|---|---|---|---|
| 2026-01-26 | Initial adherence plan approved by baseline board | architecture-working-group | ADR-001 |
