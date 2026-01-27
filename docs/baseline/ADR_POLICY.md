# ADR Policy (Baseline)

## Purpose
Define how architectural decisions are recorded, reviewed, and linked to baseline constraints, evidence, and downstream execution plans.

## When an ADR is required
Create an ADR for any decision that:
- changes baseline invariants,
- selects or changes a cloud provider, region strategy, network topology, or identity boundary,
- introduces a new material service boundary or contract,
- changes security posture (e.g., encryption, authn/authz, logging retention),
- materially changes availability, durability, or cost posture.

## ADR format (required sections)
Each ADR MUST include:
- Title (with stable ID)
- Status (Proposed / Accepted / Superseded)
- Context
- Decision
- Rationale
- Consequences
- Links (baseline constraints, adherence plan, and evidence IDs where applicable)

## Numbering and filenames
- Format: `ADR-XXX-<short-title>.md`
- Place in `docs/decisions/` if/when that directory is introduced; baseline ADRs may live in `docs/baseline/` during bootstrap.

## Review and approval
- Owner role: Architecture
- Required reviewers: Security (for security-impacting ADRs), Ops/SRE (for operability-impacting ADRs)
- Acceptance is recorded by changing the ADR Status to Accepted and noting approval date in the body.

