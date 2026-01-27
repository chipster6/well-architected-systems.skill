# Scope Boundaries (Baseline)

## In scope
- Establishing baseline governance, provider selection, and Well-Architected adherence planning for the system.
- Defining canonical doc roots, audit logs, and normalized registries.
- Producing C4 context/container baseline snapshots and foundational stubs (domain + contracts catalog).

## Out of scope
- Implementation work (coding/IaC) beyond documentation artifacts.
- Selecting a multi-cloud active/active strategy (requires a separate ADR).
- Building full contract specs and schemas (owned by `arch-docs`, once baseline gates pass).

## System boundary assumptions
- Cloud provider is the primary system-of-record provider chosen by ADR.
- External dependencies are documented in the C4 Context baseline.
- Any new external integration requires documenting boundary, data classification, and auth model prior to implementation.

## Data boundaries (high-level)
- PII and sensitive operational data must not be exposed to unauthorized parties.
- Data classification and retention requirements must be reflected in security controls and ops readiness standards.
