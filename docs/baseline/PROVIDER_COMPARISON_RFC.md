# RFC-001: Cloud Provider Comparison

## Status
Superseded (see `docs/baseline/CLOUD_PROVIDER_DECISION_ADR.md`)

## Context
The system requires global availability, strong managed streaming + IoT/edge support, and a compliance posture aligned with organizational controls. Candidate providers considered:
- AWS
- Azure
- Google Cloud Platform (GCP)

## Evaluation criteria
- Operational maturity and global footprint
- Managed services fit (IoT ingestion, streaming, storage)
- Security and identity capabilities
- Compliance program alignment
- Existing team expertise and operational readiness

## Options considered
### Option A: AWS
- Strengths: mature managed services, global regions/AZs, strong IoT + streaming ecosystem, existing team expertise.
- Risks: vendor lock-in; mitigate via contract-first interfaces and documented portability constraints.

### Option B: Azure
- Strengths: enterprise integration; strong identity ecosystem.
- Risks: team readiness and service-by-service fit for the ingestion pipeline; would require additional ramp-up.

### Option C: GCP
- Strengths: data/analytics ecosystem.
- Risks: team readiness and IoT/edge integration fit; would require additional ramp-up.

## Recommendation
Select AWS as the primary cloud provider for baseline workloads.

## Decision linkage
This RFC is finalized by `docs/baseline/CLOUD_PROVIDER_DECISION_ADR.md` (Accepted).
