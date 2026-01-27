# CloudRail Architecture Docs Agent Contract (v2)

## Non-negotiables (carry forward)
- Canada-first: default region `ca-central-1` unless a contract/governance doc explicitly permits another region.
- Contract-first: schemas and required examples must exist (or be added in the same patch) for any DM/contract reference.
- Allowed targets: `docs/**`, `contracts/schemas/**`, `contracts/examples/**` only. No file deletions or moves unless explicitly requested.
- Scripts guardrail: do not edit `./scripts/docs_verify.sh` or `./scripts/validate_schemas.sh` unless explicitly requested.
- No angle-bracket placeholders; no HTML `<br>` in Mermaid.

## MCP Call Protocol
### Preflight Gate (before drafting)
- Read this AGENTS.md plus `references/workflow.md`, `references/document-selection.md`, `references/mcp-validation.md`, `references/reference-policy.md`.
- Choose document type, then execute required MCP tools per `references/mcp-validation.md` PRE-FLIGHT matrix.
- Record each MCP call in `MCP_EVIDENCE_LOG.md` with mandatory fields (see below) before using claims in drafts.

### Postflight Gate (after drafting, before completion)
- Re-run required MCP checks per POST-FLIGHT matrix in `references/mcp-validation.md` aligned to claims made.
- Update `MCP_EVIDENCE_LOG.md` with postflight confirmations or mark sections `UNVERIFIED EXTERNALLY` if tools unavailable (blocks acceptance of normative claims).
- Ensure validation outputs for `./scripts/docs_verify.sh` and `./scripts/validate_schemas.sh` are captured when those scripts are run during doc-generation runs (not run during skill editing).

## MCP_EVIDENCE_LOG Required Fields
- source: `aws-docs` | `context7` | `terraform-awslabs` | `terraform-hashicorp` | `cdk`
- tool_used: exact MCP tool name
- query: input used
- result_summary: concise finding
- doc_link_or_identifier: URL or doc id
- how_it_changes_the_doc: what claim or section is supported/blocked
- timestamp: ISO 8601

## Claim Classification
- Source-backed: cites an MCP_EVIDENCE_LOG entry.
- Project decision: cites an ADR ID.
- Assumption: explicitly labeled; cannot be used for normative claims until converted to Source-backed or Project decision.

## Well-Architected Enforcement
- Maintain `WELL_ARCHITECTED_PILLAR_MATRIX.md` during doc generation. Each pillar (Operational Excellence, Security, Reliability, Performance Efficiency, Cost Optimization, Sustainability) must list decisions, services/patterns, risks/mitigations, and evidence pointers.

## Blocker Taxonomy
- Missing info (e.g., schema/example absent, ADR not found).
- Missing tool/access (required MCP tool unavailable).
- Irreversibility risk (operation would delete/move files or bypass governance).
