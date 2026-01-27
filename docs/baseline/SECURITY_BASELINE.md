# Security Baseline (Baseline)

## Purpose
Define baseline security expectations that all architecture and implementation plans must conform to.

## Core principles
- Least privilege: access is granted minimally and reviewed.
- Defense in depth: layered controls across identity, network, data, and monitoring.
- Secure by default: deny by default; explicit allow rules.
- Auditability: security-relevant actions are logged and traceable.

## Baseline controls (normalized)
Canonical control catalog lives in:
- `registries/security_controls_catalog.yml`

Baseline minimum control (initial):
- `SECCTRL-0001` Least privilege access

## Data protection expectations (baseline)
- Sensitive data must be protected in transit and at rest using approved mechanisms for the chosen provider.
- Secrets must not be committed to the repository.

