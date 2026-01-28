---
name: arch-baseline
version: "1.0"
description: >
  Establish project baseline governance, provider decision, post-decision research normalization, and Well-Architected adherence plan; emit a hard gate for downstream skills.
  Triggers: "baseline", "arch-baseline", "provider decision", "cloud provider", "Well-Architected plan", "baseline gate", "validate_baseline.py", "scaffold_baseline.py".
  Fails closed on missing mandatory artifacts or empty required controls.
---

# arch-baseline — Baseline Governance + Provider Decision + Research-Normalized Well-Architected Plan

## Mission
Reduce architectural variance by anchoring the project to project-specific ground truth, then producing a validated baseline system-of-record that downstream skills must reference.

## Scope
This skill produces baseline governance, scope boundaries, provider decision (RFC→ADR), post-decision research with audit trail, Well-Architected adherence plan, C4 Context/Container snapshot, and baseline stubs for domain model and contract catalog. It also initializes canonical registries.

## Non-negotiable invariants
1. **Baseline-first**: Downstream skills must fail if baseline gate fails.
2. **Fail-closed validation**: Missing mandatory artifacts or empty required controls cause failure.
3. **Auditable research**: Every external lookup is recorded in the tool-call audit trail and referenced in the evidence log.
4. **Normalization**: Research findings must land in registries/policies—not just narrative docs.
5. **Decision lifecycle**: Provider choice and major baseline deviations are recorded as RFC→ADR (or Exception/ACR if you implement it later).

## Canonical output locations (project repo)
- Baseline docs: `docs/baseline/`
- Architecture docs: `docs/architecture/` (owned by arch-docs)
- Implementation docs: `docs/implementation/` (owned by impl-strategy)
- Canonical registries: `registries/`
- Audit artifacts: `docs/audit/`
  - Evidence: `docs/audit/evidence/`
  - Tool-call audit: `docs/audit/tool_calls/`

## Mandatory baseline artifacts (project outputs)
Baseline governance and standards:
- `docs/baseline/DOCS_GOVERNANCE.md`
- `docs/baseline/ADR_POLICY.md`
- Golden templates directory (project-level reference): `docs/baseline/golden_templates/`

System definition:
- `docs/baseline/SYSTEM_CHARTER.md`
- `docs/baseline/SCOPE_BOUNDARIES.md`

Provider evaluation and decision:
- `docs/baseline/PROVIDER_COMPARISON_RFC.md`
- `docs/baseline/CLOUD_PROVIDER_DECISION_ADR.md`

Post-decision research + adherence:
- `docs/baseline/WELL_ARCHITECTED_ADHERENCE_PLAN.md`
- `docs/audit/EVIDENCE_LOG.md`
- `docs/audit/tool_calls/tool_call_audit.jsonl` (required)

Baseline architecture snapshot + stubs:
- `docs/baseline/C4_Context.md`
- `docs/baseline/C4_Container.md`
- `docs/baseline/DOMAIN_MODEL.md` (initialized stub)
- `docs/baseline/CONTRACT_CATALOG.md` (initialized stub)

Security and operational baselines:
- `docs/baseline/SECURITY_BASELINE.md`
- `docs/baseline/OPS_READINESS_STANDARD.md`

Handoff contract to downstream skill:
- `docs/baseline/BASELINE_INDEX.md`
- `docs/baseline/BASELINE_HANDOFF.md`
- `docs/baseline/baseline_manifest.json`

Registries (canonical truth):
- `registries/constraints_registry.yml` (or .json)
- `registries/security_controls_catalog.yml` (or .json)
- `registries/slo_catalog.yml` (or .json)
- Optional early catalogs (initialize empty if applicable):
  - `registries/service_catalog.yml`
  - `registries/event_catalog.yml`
  - `registries/env_catalog.yml`

## Provider packs
After provider selection, load a provider pack and normalize guidance into registries and adherence plan.
Recommended location:
- `custom_skills/arch-baseline/resources/provider_packs/aws/`
- `custom_skills/arch-baseline/resources/provider_packs/azure/`
- `custom_skills/arch-baseline/resources/provider_packs/gcp/`

Each pack should contain:
- pillar sets + review procedure defaults
- baseline control mappings (identity, logging, encryption, monitoring)
- naming/structural constraints (accounts/subscriptions/projects, regions, network)
- validation extensions for the baseline gate

## Research sources (post provider decision)
Use MCP documentation tools when available, otherwise web search. Record all lookups:
- Cloud provider docs MCP (AWS/Azure/GCP depending on chosen provider)
- Kubernetes docs MCP (if Kubernetes is in scope)
- Terraform docs MCP (if Terraform is in scope)
- AWS CDK docs MCP (if CDK is in scope)
- Additional sources only if required; always logged.

## Execution contract (high-level)
Follow phases and gates defined in `phased_artifact_workflow+gates.md`.
Stop immediately if any gate fails. Do not proceed to downstream skills until the baseline gate passes.

## Quality bar
- No invented claims about provider best practices without recorded evidence.
- No missing mandatory artifacts.
- Registries contain normalized constraints/controls sufficient to govern downstream docs.
- Adherence plan maps every pillar to required downstream deliverables and evidence types.
