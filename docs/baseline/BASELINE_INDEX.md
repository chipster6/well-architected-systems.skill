# Baseline Index

This index is the authoritative entrypoint for all baseline artifacts. Downstream skills (arch-docs, impl-strategy) MUST reference this index and the baseline manifest.

## Baseline metadata
- Baseline ID:
- Baseline status: draft | published
- Provider: aws | azure | gcp
- Provider guidance review date (UTC):
- Toolchain applicability:
  - Kubernetes: yes | no
  - Terraform: yes | no
  - CDK: yes | no
- Owner:
- Last updated (UTC):

## Canonical truth locations
- Baseline docs: `docs/baseline/`
- Architecture docs: `docs/architecture/`
- Implementation docs: `docs/implementation/`
- Registries (system of record): `registries/`
- Audit artifacts: `docs/audit/`
  - Evidence: `docs/audit/evidence/`
  - Tool-call audit: `docs/audit/tool_calls/`

## Phase completion status
Mark complete only when the corresponding gate has passed.

- [ ] B0 Governance + Canonicalization passed
- [ ] B1 System definition passed
- [ ] B2 Provider decision passed
- [ ] B3 Provider pack + toolchain applicability passed
- [ ] B4 Research + normalization passed
- [ ] B5 Well-Architected adherence plan passed
- [ ] B6 C4 snapshot + domain/contract initialization passed
- [ ] B7 Security/ops + handoff + publication passed

## Baseline artifacts (authoritative links)

### Governance and standards (B0)
- DOCS_GOVERNANCE: `docs/baseline/DOCS_GOVERNANCE.md`
- ADR_POLICY: `docs/baseline/ADR_POLICY.md`
- Golden templates: `docs/baseline/golden_templates/`

### System definition (B1)
- SYSTEM_CHARTER: `docs/baseline/SYSTEM_CHARTER.md`
- SCOPE_BOUNDARIES: `docs/baseline/SCOPE_BOUNDARIES.md`

### Provider evaluation and decision (B2)
- PROVIDER_COMPARISON_RFC: `docs/baseline/PROVIDER_COMPARISON_RFC.md`
- CLOUD_PROVIDER_DECISION_ADR: `docs/baseline/CLOUD_PROVIDER_DECISION_ADR.md`

### Toolchain + provider pack (B3)
- TOOLCHAIN_BASELINE: `docs/baseline/TOOLCHAIN_BASELINE.md`
- Provider pack (reference): `custom_skills/arch-baseline/resources/provider_packs/<provider>/`

### Research + normalization (B4)
- Evidence log (human): `docs/audit/EVIDENCE_LOG.md`
- Evidence log (machine): `docs/audit/evidence/evidence_log.jsonl`
- Tool-call audit (machine): `docs/audit/tool_calls/tool_call_audit.jsonl`
- Tool-call audit summary: `docs/audit/tool_calls/TOOL_CALL_AUDIT_SUMMARY.md`

### Well-Architected adherence plan (B5)
- WELL_ARCHITECTED_ADHERENCE_PLAN: `docs/baseline/WELL_ARCHITECTED_ADHERENCE_PLAN.md`

### Architecture snapshot + initialization (B6)
- C4_Context: `docs/baseline/C4_Context.md`
- C4_Container: `docs/baseline/C4_Container.md`
- DOMAIN_MODEL (baseline stub): `docs/baseline/DOMAIN_MODEL.md`
- CONTRACT_CATALOG (baseline stub): `docs/baseline/CONTRACT_CATALOG.md`

### Security and ops baselines (B7)
- SECURITY_BASELINE: `docs/baseline/SECURITY_BASELINE.md`
- OPS_READINESS_STANDARD: `docs/baseline/OPS_READINESS_STANDARD.md`

### Handoff and publication (B7)
- BASELINE_HANDOFF: `docs/baseline/BASELINE_HANDOFF.md`
- Baseline manifest: `docs/baseline/baseline_manifest.json`

## Registries (system of record)
- Constraints registry: `registries/constraints_registry.yml`
- Security controls catalog: `registries/security_controls_catalog.yml`
- SLO catalog: `registries/slo_catalog.yml`
- Service catalog (if applicable): `registries/service_catalog.yml`
- Event catalog (if applicable): `registries/event_catalog.yml`
- Environment catalog (if applicable): `registries/env_catalog.yml`

## Notes / open items
If you need to track unknowns without placeholders, list them here as actionable items with IDs and a target resolution phase.
- OI-0001:
- OI-0002:
