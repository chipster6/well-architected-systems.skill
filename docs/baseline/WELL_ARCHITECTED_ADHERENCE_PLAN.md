---
doc_id: WELLARCH-BASE-001
doc_type: well_architected_adherence_plan
status: draft
phase: baseline
provider: aws
framework_name: AWS Well-Architected Framework
framework_version: latest reviewed 2026-01-15
owner: architecture-working-group
review_cadence: monthly
last_reviewed: 2026-01-20
next_review_due: 2026-02-20
related_docs:
  - docs/baseline/SYSTEM_CHARTER.md
  - docs/baseline/C4_Context.md
  - docs/baseline/C4_Container.md
  - docs/baseline/CLOUD_PROVIDER_DECISION_ADR.md
evidence_log: docs/audit/EVIDENCE_LOG.md
---

# Well-Architected Adherence Plan

## 1. Purpose
Define how the system satisfies the AWS Well-Architected Framework, including pillar ownership, review cadence, evidence expectations, and the baseline gate used by downstream skills.

## 2. Framework Selection
- **Provider:** aws
- **Framework name:** AWS Well-Architected Framework
- **Framework version / review date:** latest reviewed 2026-01-15
- **Scope of adherence:** entire_system

## 3. Definitions
- **Pillar:** AWS prescriptive guidance area (Operational Excellence, Security, Reliability, Performance Efficiency, Cost Optimization).
- **Control / Practice:** A measurable requirement mapped to a pillar.
- **Evidence:** Artifacts demonstrating implementation (IaC, logs, configs, ADRs, test runs).
- **Exception:** Approved deviation with compensating controls and expiry.

## 4. Pillar-to-Documentation Mapping (Required)
Populate all pillars for the chosen provider. Each row is a commitment that must be satisfied or explicitly waived.

| Pillar | Mandatory? (Y/N) | Key Practices / Controls (summary) | Required Architecture Docs / Sections | Required Evidence Types | Owner | Review Cadence |
|---|---:|---|---|---|---|---|
| Operational Excellence | Y | IaC pipelines, standardized runbooks, automated drift detection | docs/architecture/ops/RUNBOOK.md | CI job logs, drift reports, runbook revisions | operations-lead | monthly |
| Security | Y | IAM least privilege, encryption, network segmentation | docs/architecture/security/THREAT_MODEL.md | IAM policy diffs, KMS config, VPC diagrams | security-lead | monthly |
| Reliability | Y | Multi-AZ deployments, backup testing, chaos drills | docs/architecture/reliability.md | Backup reports, failover test logs, chaos runbooks | reliability-lead | monthly |
| Performance Efficiency | Y | Right-sized compute, telemetry-driven scaling, caching | docs/architecture/performance.md | Load tests, autoscaling metrics, cache hit ratios | performance-lead | quarterly |
| Cost Optimization | Y | Tagging, budget alarms, capacity reviews | docs/architecture/cost.md | Cost Explorer exports, tagging compliance scans | finance-liaison | quarterly |

## 5. Baseline Requirements (Non-Negotiable)
These requirements apply regardless of provider. If compliance is not possible, an exception must be logged.

### 5.1 Security Baseline
- Enforce least-privilege IAM roles with session tagging and CloudTrail auditing.
- Encrypt all data at rest with AWS KMS CMKs; enforce TLS 1.2+ for data in transit.
- Forward security logs to the audit account with retention >= 400 days.
- Apply data classification labels to every dataset; restrict PII movement between accounts.

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
- Pillar table covers all AWS pillars with owners and cadences.
- Evidence storage locations exist and are accessible.
- Exception workflow is documented and linked to ADRs.
- Related baseline documents exist and link to this plan.

## 10. Change Log
| Date | Change | Author | Reference (ADR/RFC) |
|---|---|---|---|
| 2026-01-26 | Initial adherence plan approved by baseline board | architecture-working-group | ADR-001 |
