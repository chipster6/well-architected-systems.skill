# Operations Readiness Standard (Baseline)

## Purpose
Define minimum operational readiness expectations for services and workflows to ensure reliable delivery.

## SLO baseline
Canonical SLO catalog lives in:
- `registries/slo_catalog.yml`

Baseline initial SLO:
- `SLO-0001` API availability (placeholder-free, measurable target)

## Observability expectations
- Services must emit metrics and logs sufficient to measure SLOs and diagnose incidents.
- Alerting thresholds should be derived from SLOs where practical.

## Incident response expectations
- Each material service must have a runbook covering common failure modes and escalation paths.
- Post-incident reviews should produce actionable follow-ups tracked in implementation strategy.

