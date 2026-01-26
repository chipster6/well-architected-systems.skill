# Verification Guide

This document provides verification commands to test the custom agent skills repository with baseline-first governance.

## Quick Test Commands

### 1. Test Baseline Gate (Expected Failure - Provider=TBD)

```bash
# Create test directory and copy template
mkdir -p docs/baseline
cp custom_skills/arch-baseline/resources/templates/baseline/WELL_ARCHITECTED_ADHERENCE_PLAN.md docs/baseline/

# Run baseline gate (should fail)
python custom_skills/arch-baseline/scripts/validate_baseline.py
```

**Expected Output:**
```
=== BASELINE GATE VALIDATION ===

1. Checking required baseline files...
✗ System Charter missing: docs/baseline/SYSTEM_CHARTER.md
✗ C4 Context Diagram missing: docs/baseline/C4_Context.md
✗ C4 Container Diagram missing: docs/baseline/C4_Container.md
✗ Cloud Provider Decision ADR missing: docs/baseline/CLOUD_PROVIDER_DECISION_ADR.md

2. Validating Well-Architected Adherence Plan...
✗ Well-Architected Adherence Plan validation failed

=== BASELINE GATE RESULT ===
✗ BASELINE GATE FAILED - Fix issues before proceeding
```

### 2. Test Baseline Gate (Expected Success - Provider=AWS + Pillars Filled)

```bash
# Create a valid Well-Architected Adherence Plan
cat > docs/baseline/WELL_ARCHITECTED_ADHERENCE_PLAN.md << 'EOF'
---
doc_id: WELLARCH-BASE-001
doc_type: well_architected_adherence_plan
status: draft
phase: baseline
provider: aws
framework_name: AWS Well-Architected Framework
framework_version: latest reviewed 2026-01-25
owner: architecture-team
review_cadence: monthly
last_reviewed: 2026-01-25
next_review_due: 2026-02-25
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
- **Provider:** aws
- **Framework name:** AWS Well-Architected Framework
- **Framework version / review date:** latest reviewed 2026-01-25
- **Scope of adherence:** entire_system

## 3. Definitions
- **Pillar:** A category of architectural guidance (provider-specific).
- **Control / Practice:** A concrete requirement or recommendation mapped to a pillar.
- **Evidence:** A verifiable artifact showing implementation/adherence (config, logs, tests, IaC, runbooks, etc.).
- **Exception:** An approved deviation with a documented rationale and compensating controls.

## 4. Pillar-to-Documentation Mapping (Required)
| Pillar | Mandatory? (Y/N) | Key Practices / Controls (summary) | Required Architecture Docs / Sections | Required Evidence Types | Owner | Review Cadence |
|---|---:|---|---|---|---|---|
| Operational Excellence | Y | Infrastructure as Code, Monitoring | docs/architecture/ops-excellence.md | Config files, Metrics | ops-team | monthly |
| Security | Y | IAM, Encryption, Network Security | docs/architecture/security.md | IAM policies, Security groups | security-team | monthly |
| Reliability | Y | Backup, Multi-AZ, Failover | docs/architecture/reliability.md | Backup configs, Test results | reliability-team | monthly |
| Performance Efficiency | Y | Scaling, Caching, Optimization | docs/architecture/performance.md | Load tests, Metrics | performance-team | monthly |
| Cost Optimization | Y | Resource tagging, Rightsizing | docs/architecture/cost.md | Cost reports, Tags | finance-team | monthly |

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
- **Milestone review:** occurs at each major release
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
- Evidence log: `docs/audit/EVIDENCE_LOG.md`
- IaC references: `infrastructure/`
- Config snapshots: `configs/`
- Test results: `tests/`

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
| 2026-01-25 | Initial baseline plan | Architecture Team | ADR-001 |
EOF

# Create placeholder files for other required docs
touch docs/baseline/SYSTEM_CHARTER.md
touch docs/baseline/C4_Context.md
touch docs/baseline/C4_Container.md
touch docs/baseline/CLOUD_PROVIDER_DECISION_ADR.md

# Run baseline gate (should pass)
python custom_skills/arch-baseline/scripts/validate_baseline.py
```

**Expected Output:**
```
=== BASELINE GATE VALIDATION ===

1. Checking required baseline files...
✓ System Charter exists: docs/baseline/SYSTEM_CHARTER.md
✓ C4 Context Diagram exists: docs/baseline/C4_Context.md
✓ C4 Container Diagram exists: docs/baseline/C4_Container.md
✓ Cloud Provider Decision ADR exists: docs/baseline/CLOUD_PROVIDER_DECISION_ADR.md

2. Validating Well-Architected Adherence Plan...
✓ Well-Architected Adherence Plan validation passed

=== BASELINE GATE RESULT ===
✓ BASELINE GATE PASSED - All requirements satisfied
Ready to proceed with arch-docs and impl-strategy
```

### 3. Test Arch-Docs Baseline Dependency

```bash
# Test arch-docs with baseline passing
python custom_skills/arch-docs/scripts/validate_docs.py
```

**Expected Output:**
```
=== ARCH-DOCS VALIDATION ===
=== CHECKING BASELINE GATE ===
✓ BASELINE GATE PASSED

=== PROCEEDING WITH DOCUMENTATION VALIDATION ===
! Architecture directory not found: docs/architecture
! This is expected for new repositories
✓ Documentation validation placeholder passed
```

### 4. Test Impl-Strategy Baseline Dependency

```bash
# Test impl-strategy with baseline passing
python custom_skills/impl-strategy/scripts/validate_task_graph.py
```

**Expected Output:**
```
=== IMPLEMENTATION STRATEGY VALIDATION ===
=== CHECKING BASELINE GATE ===
✓ BASELINE GATE PASSED

=== PROCEEDING WITH TASK GRAPH VALIDATION ===
! Implementation directory not found: docs/implementation
! This is expected for new repositories
✓ Task graph validation placeholder passed
```

### 5. Test Baseline Gate Failure Blocking

```bash
# Remove required files to test failure
rm docs/baseline/SYSTEM_CHARTER.md

# Test arch-docs with baseline failing
python custom_skills/arch-docs/scripts/validate_docs.py
```

**Expected Output:**
```
=== ARCH-DOCS VALIDATION ===
=== CHECKING BASELINE GATE ===
✗ BASELINE GATE FAILED
[... validation errors ...]

BASELINE GATE FAILED
Architecture documentation cannot proceed until baseline passes.
```

### 6. Test Wrapper Script

```bash
# Test the shell wrapper
./tools/run_baseline_gate.sh
```

**Expected Output:** Same as direct Python call (pass or fail depending on file state)

## Cleanup Test Files

```bash
# Clean up test files
rm -rf docs/baseline/
```

## Validation Checklist

- [ ] Baseline gate fails with provider=tbd
- [ ] Baseline gate fails with missing required files  
- [ ] Baseline gate passes with valid provider and pillar data
- [ ] Arch-docs blocked when baseline fails
- [ ] Impl-strategy blocked when baseline fails
- [ ] Both skills pass when baseline gate passes
- [ ] GitHub Actions workflows exist and are syntactically valid
- [ ] All scripts use Python standard library only
- [ ] No network calls required for validation