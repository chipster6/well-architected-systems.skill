# ADR-001: Select AWS as the Primary Cloud Provider

## Status
Accepted

## Context
The system requires global availability, mature managed services, and an operational/compliance posture aligned with organizational controls. Candidate providers were AWS, Azure, and GCP.

## Decision
Adopt AWS as the system-of-record provider for all baseline workloads. Azure and GCP remain evaluation targets for future redundancy, but all governance artifacts assume AWS primitives.

## Rationale
- Existing operations team holds AWS expertise and runbooks.
- AWS provides validated IoT Core + Kinesis pipeline capabilities with managed scaling.
- Compliance (ISO 45001, ISO 27001, SOC 2) already mapped to corporate controls.

## Consequences
- All reference architectures, security controls, and implementation strategies must align with AWS terminology.
- Any multi-cloud initiative requires a separate ADR plus dependency impact review.
