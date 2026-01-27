# Reference Policy (CloudRail Arch Docs v2)

## Minimum Reference Set by Document Type
- ADR / ARC / SERVICE / WORKFLOW: include GOV-ARCH-001 index entry, related ADRs, and MCP evidence for normative claims.
- DM / DCON / API: include linked schemas in `contracts/schemas/` and examples in `contracts/examples/`; cite MCP evidence for service limits, data residency, encryption, and SLAs.
- SECURITY / OBS / DR / RUN: include applicable ADRs plus MCP evidence for AWS controls, quotas, and service behaviors.
- GOV / REF: include governing ADRs and MCP evidence when asserting cloud behaviors or limits.

## MCP Citation Requirement
- Any normative cloud/service/IaC claim must be Source-backed with an `MCP_EVIDENCE_LOG.md` entry. Each entry must include `evidence_id` formatted as `MCP-YYYYMMDD-NNNN` (4-digit zero-padded sequence).
- Project decisions must cite ADR IDs.
- Assumptions must be labeled and cannot satisfy acceptance criteria.

## Evidence Referencing
- References sections in documents must list the evidence_id(s) for Source-backed claims, e.g., `MCP Evidence IDs used: [MCP-20260124-0001, MCP-20260124-0002]`.

## Canonical Internal References
- `docs/09_GOVERNANCE/GOV-ARCH-001-Architecture-Documentation-Index.md` must be updated when ARC, DM, SERVICE, or WORKFLOW docs change.
- `docs/03_CONTRACTS/REGISTRY.md` must align with DM/DCON/API references.
