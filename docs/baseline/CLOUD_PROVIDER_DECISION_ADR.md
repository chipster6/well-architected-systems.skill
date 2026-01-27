# ADR-001: Cloud Provider Decision (Template)

## Status
Template

## Context
The system requires global availability, mature managed services, and an operational/compliance posture aligned with organizational controls. Candidate providers were AWS, Azure, and GCP.

## Decision
This ADR records the chosen primary cloud provider for a specific project run. When used in a real project baseline, replace this template section with the selected provider and the scope of that decision (e.g., which environments/workloads are in-scope).

## Rationale
Document the reasoned tradeoffs that led to the decision, including:
- team readiness and operating model
- service fit for required workloads
- security and compliance considerations
- cost and performance posture
- portability constraints and mitigations

## Consequences
Once a provider is selected for a project run:
- Provider packs become authoritative for pillar mapping and doc family requirements.
- Downstream docs and implementation strategy must align with the selected provider’s terminology and Well-Architected framework.
- Any multi-cloud initiative requires a separate ADR plus dependency impact review.
