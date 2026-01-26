---
doc_id: WELLARCH-BASE-001
doc_type: well_architected_adherence_plan
status: draft              # draft|approved|superseded
phase: baseline
provider: tbd              # aws|azure|gcp|tbd
framework_name: TBD        # e.g., "AWS Well-Architected Framework", "Azure Well-Architected Framework", "Google Cloud Architecture Framework"
framework_version: TBD     # e.g., "latest reviewed YYYY-MM-DD" or a provider-published version label
owner: TBD
review_cadence: TBD        # e.g., "per milestone", "monthly", "pre-prod"
last_reviewed: TBD         # YYYY-MM-DD
next_review_due: TBD       # YYYY-MM-DD
related_docs:
  - docs/baseline/SYSTEM_CHARTER.md
  - docs/baseline/C4_Context.md
  - docs/baseline/C4_Container.md
  - docs/baseline/CLOUD_PROVIDER_DECISION_ADR.md
evidence_log: docs/audit/EVIDENCE_LOG.md
---

# Well-Architected Adherence Plan

## 1. Purpose
State how this project will adhere to the selected cloud provider's well-architected framework, including pillars, review process, evidence expectations, and exception handling.

## 2. Framework Selection
- **Provider:** aws|azure|gcp
- **Framework name:** {{name}}
- **Framework version / review date:** {{version_or_date}}
- **Scope of adherence:** {{entire_system|subset}} (if subset, define boundaries)

## 3. Definitions
- **Pillar:** A category of architectural guidance (provider-specific).
- **Control / Practice:** A concrete requirement or recommendation mapped to a pillar.
- **Evidence:** A verifiable artifact showing implementation/adherence (config, logs, tests, IaC, runbooks, etc.).
- **Exception:** An approved deviation with a documented rationale and compensating controls.

## 4. Pillar-to-Documentation Mapping (Required)
Populate all pillars for the chosen provider. Each row is a commitment that must be satisfied or explicitly waived.

| Pillar | Mandatory? (Y/N) | Key Practices / Controls (summary) | Required Architecture Docs / Sections | Required Evidence Types | Owner | Review Cadence |
|---|---:|---|---|---|---|---|
| {{pillar_1}} | Y | {{controls}} | {{docs/sections}} | {{evidence_types}} | {{owner}} | {{cadence}} |
| {{pillar_2}} | Y | {{controls}} | {{docs/sections}} | {{evidence_types}} | {{owner}} | {{cadence}} |
| {{pillar_3}} | Y | {{controls}} | {{docs/sections}} | {{evidence_types}} | {{owner}} | {{cadence}} |

## 5. Baseline Requirements (Non-Negotiable)
These requirements apply regardless of provider. If you cannot comply, you must file an exception.

### 5.1 Security Baseline
- Identity and access management baseline (least privilege, roles, auditability)
- Encryption baseline (at rest + in transit; key management)
- Logging/auditing baseline (security logs retained; access trails)
- Data classification and handling rules

### 5.2 Reliability Baseline
- Availability targets (SLO intent)
- Backup and recovery posture (RTO/RPO intent)
- Failure mode considerations and resiliency posture

### 5.3 Operational Excellence Baseline
- Operational readiness definition
- Runbook requirements
- Incident response hooks and escalation path

## 6. Review Procedure
Describe how you will execute well-architected reviews and capture results.

### 6.1 Review Events
- **Baseline review:** occurs when baseline artifacts are approved
- **Milestone review:** occurs at {{milestone definition}}
- **Pre-production review:** occurs before production cutover

### 6.2 Review Output Artifacts
- Review summary (findings, risks)
- Remediation plan (prioritized)
- Evidence updates (links/IDs)
- Decision records (ADRs) for significant changes

## 7. Evidence and Audit Rules
### 7.1 Evidence ID Format
- Evidence IDs follow: `EVD-YYYYMMDD-NNNN` (example: `EVD-20260125-0001`)

### 7.2 Evidence Locations
- Evidence log: `{{path}}`
- IaC references: `{{path}}`
- Config snapshots: `{{path}}`
- Test results: `{{path}}`

### 7.3 Traceability Requirements
Each pillar row must map to:
- at least one architecture doc/section, and
- at least one evidence item (or a declared planned evidence item with due date).

## 8. Exception / Waiver Process
- An exception must be documented with:
  - RFC (proposal) + ADR (decision) OR ACR (if using formal change governance)
  - rationale
  - compensating controls
  - expiry date / re-evaluation date

## 9. Acceptance Criteria (Baseline Gate)
Baseline is not approved unless:
- Provider and framework are set (not TBD)
- Pillar mapping table is complete (no placeholders)
- Evidence locations are defined
- Exception process is defined
- Related baseline docs exist and are linked

## 10. Change Log
| Date | Change | Author | Reference (ADR/RFC) |
|---|---|---|---|
| {{YYYY-MM-DD}} | {{summary}} | {{name}} | {{ADR/RFC}} |