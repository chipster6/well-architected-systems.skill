# Quality Gates (Definition of Done)

## Structure Gate
- Document must include Purpose, Scope, References, Acceptance Criteria.

## Contract Gate
- Schemas/examples referenced must exist and be aligned with `contracts/schemas/` and `contracts/examples/`.
- Update `docs/03_CONTRACTS/REGISTRY.md` when contracts change.

## Consistency Gate
- Naming matches governance; Control Plane vs Tenant Plane boundaries are explicit.
- Regional defaults honor `ca-central-1` unless contractually overridden.

## MCP Gate
- `MCP_EVIDENCE_LOG.md` present and populated for normative claims.
- Preflight and postflight MCP calls executed per `references/mcp-validation.md`.
- Sections lacking required evidence marked `UNVERIFIED EXTERNALLY` (blocks acceptance).

## TOKEN_REPLACEMENT_GATE
- Final docs must contain **no** `TOKEN_*` markers and **no** angle brackets (`<` or `>`). Templates may carry tokens, but publication requires full replacement.

## Well-Architected Gate
- `WELL_ARCHITECTED_PILLAR_MATRIX.md` completed covering all six pillars with decisions, risks/mitigations, evidence pointers.

## DOC_SEQUENCE_GATE
**Pass criteria (objective):**
- Phase report declares `build_mode` (greenfield|incremental)
- If `build_mode=greenfield`:
  - Phase report declares `sequence_block` (A|B|C|D|E|F|G)
  - Changed docs/contract files are within allowed blocks (<= current block), OR a WAIVER exists
- If WAIVER exists:
  - WAIVER rationale + backfill plan present in the phase report
  - Impacted dependencies documented in WAIVER section

## Validation Scripts Gate
- Applies only when docs/** or contracts/** are modified in a doc-generation run.
- Capture PASS outputs for `./scripts/docs_verify.sh` and `./scripts/validate_schemas.sh` (scripts themselves not modified in this skill update).
