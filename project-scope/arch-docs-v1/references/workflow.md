# CloudRail Architecture Documentation Workflow

This workflow governs how CloudRail documentation is created and updated. It is contract-first, evidence-by-construction, and validation-gated.

## Preflight Checklist (Required)
1. Read `AGENTS.md` (governance, MCP call protocol) and `references/mcp-validation.md`.
2. Read `references/document-selection.md`, `references/reference-policy.md`, and templates index at `references/templates.md`.
3. Read `docs/09_GOVERNANCE/GOV-ARCH-001-Architecture-Documentation-Index.md` and `docs/03_CONTRACTS/REGISTRY.md`.
4. Confirm allowed targets are limited to `docs/**`, `contracts/schemas/**`, and `contracts/examples/**` unless explicitly expanded.
5. Confirm Canada-first defaults (`ca-central-1`) unless a contract explicitly allows another region.
6. Execute MCP PRE-FLIGHT calls per `references/mcp-validation.md` for selected doc type; log entries in `MCP_EVIDENCE_LOG.md` before drafting normative claims.

## Documentation Creation Workflow (Phases P0-P6)

### Phase P0: Intake & Governance
**Purpose:** Establish governance context and permission to proceed
**Entry Gates (must exist/read before starting):**
- `docs/09_GOVERNANCE/GOV-ARCH-001-Architecture-Documentation-Index.md` must exist and be readable
- `docs/03_CONTRACTS/REGISTRY.md` must exist and be readable  
- All relevant ADRs listed in GOV-ARCH-001 must be accessible
- MCP evidence prerequisites completed for any normative claims (per `references/mcp-validation.md`)
**Build Mode + Sequence Gate:**
- Declare `build_mode`: `greenfield` | `incremental`
- If `build_mode=greenfield`: Declare current `sequence_block`: `A`|`B`|`C`|`D`|`E`|`F`|`G`
- If `build_mode=greenfield`: Must follow `references/doc-build-sequence.md` for the declared sequence block
- Document build mode and sequence selection in `PHASE_COMPLETION_REPORT_P0.md`
**Outputs Produced:**
- Initial `MCP_EVIDENCE_LOG.md` with preflight entries
- Initial `WELL_ARCHITECTED_PILLAR_MATRIX.md` with baseline state
- `PHASE_COMPLETION_REPORT_P0.md` documenting governance intake, build_mode, and sequence_block
**Exit Gates (must pass before P1):**
- All governance documents successfully read and parsed
- Pre-flight MCP calls executed and logged
- No missing prerequisite ADRs or governance gaps identified
- Build mode and sequence declaration complete (for greenfield)

### Phase P1: Decision Inputs & Requirements
**Purpose:** Gather all decision inputs and technical constraints
**Entry Gates:**
- P0 completion report approved
- All source ADRs identified and accessible
- Service limits and constraints researched via MCP tools when making normative claims
**Outputs Produced:**
- Requirements analysis document (internal)
- Updated `MCP_EVIDENCE_LOG.md` with decision-input evidence
- Risk assessment for technical choices
**Exit Gates:**
- All normative technical claims have MCP evidence logged
- Source ADRs reviewed and cited
- Technical constraints documented with evidence

### Phase P2: Architecture & Data Modeling
**Purpose:** Design system architecture and data contracts
**Entry Gates:**
- P1 completion report approved
- Schema-first requirements satisfied for any DM docs
- Required schemas exist in `contracts/schemas/` before writing DM docs
**Outputs Produced:**
- `docs/02_ARCHITECTURE/ARC-*.md` (system architecture)
- `docs/03_CONTRACTS/DM-*.md` (data models) if applicable
- `docs/03_CONTRACTS/REGISTRY.md` updates for new schemas
- `contracts/schemas/*.schema.json` for new data models
- `contracts/examples/**` for all new schemas
**Exit Gates:**
- All data models have corresponding schemas and examples
- Architecture decisions documented with evidence
- Schema validation passes for all new schemas

### Phase P3: Service & Workflow Design
**Purpose:** Define service interfaces and workflow orchestration
**Entry Gates:**
- P2 completion report approved
- All architecture decisions from P2 are incorporated
**Outputs Produced:**
- `docs/04_SERVICES/SERVICE_*.md` (service specifications)
- `docs/05_WORKFLOWS/WORKFLOW_*.md` (workflow specifications)
- `docs/05_WORKFLOWS/RUNNER_CONTRACT.md` (runner interfaces)
**Exit Gates:**
- Service contracts reference valid architecture from P2
- Workflow designs reference correct service interfaces
- All external dependencies documented with MCP evidence

### Phase P4: Security & Operations Design
**Purpose:** Define security controls and operational procedures
**Entry Gates:**
- P3 completion report approved
- All service interfaces from P3 are finalized
**Outputs Produced:**
- `docs/07_OPERATIONS/*.md` (security, observability, DR, runbooks, test strategies)
- Updated security control matrix
- Operational readiness checklists
**Exit Gates:**
- Security controls align with Well-Architected Framework
- All operational procedures reference valid services
- Monitoring and alerting strategies documented

### Phase P5: Documentation Quality & Validation
**Purpose:** Apply quality gates and prepare documentation for publication
**Entry Gates:**
- P4 completion report approved
- All content drafts are complete
**Outputs Produced:**
- Updated `MCP_EVIDENCE_LOG.md` with post-flight MCP calls
- Updated `WELL_ARCHITECTED_PILLAR_MATRIX.md` with final decisions
- Quality gate compliance report
**Exit Gates:**
- `references/quality-gates.md` compliance verified (Structure, Contract, Consistency, MCP, TOKEN_REPLACEMENT, Well-Architected)
- `references/reference-policy.md` compliance verified (claim classification, evidence_id format)
- MCP POST-FLIGHT calls executed for all normative claims
- No TOKEN_* markers or angle brackets remain in final docs

### Phase P6: Publication & Integration
**Purpose:** Finalize documentation and update governance indexes
**Entry Gates:**
- P5 completion report approved
- All quality gates passed
**Outputs Produced:**
- Updated `docs/09_GOVERNANCE/GOV-ARCH-001-Architecture-Documentation-Index.md`
- Final `PHASE_COMPLETION_REPORT_P6.md` with build mode and sequence compliance
- Complete change set with all required artifacts
**Exit Gates:**
- GOV-ARCH-001 updated with all new ARC/DM/SERVICE/WORKFLOW docs
- REGISTRY.md updated with all new contracts/schemas
- All validation scripts show PASS (when docs/** or contracts/** modified)
- All phase completion reports generated and validated
- Build mode compliance documented:
  - If `build_mode=greenfield`: sequence compliance declared (compliant|waiver)
  - If `sequence_compliance=waiver`: waiver rationale and backfill plan present in P6 report

## Required Reporting Artifacts
Every documentation creation run must produce:
- `PHASE_COMPLETION_REPORT_P0.md` through `PHASE_COMPLETION_REPORT_P6.md` (one per completed phase)
- `MCP_EVIDENCE_LOG.md` updates when normative claims are introduced or modified
- `WELL_ARCHITECTED_PILLAR_MATRIX.md` updates when architecture decisions are made
- `CLAIM_INDEX` updates when claims are added or changed (if applicable to this repo's workflow)

## Schema-First Gate (Required for DM Docs)
Before writing any `docs/03_CONTRACTS/DM-*.md` document:
- Verify each referenced schema exists in `contracts/schemas/`.
- Verify required examples exist under `contracts/examples/`.
- If schema or examples are missing and are not created in the same patch set, stop and output `BLOCKER` with the exact missing files.
- Update `docs/03_CONTRACTS/REGISTRY.md` in the same patch when introducing new DM docs or schemas.

## Governance Index Gate
- When adding ADR, ARC, SERVICE, or WORKFLOW docs, update `docs/09_GOVERNANCE/GOV-ARCH-001-Architecture-Documentation-Index.md` in the same patch.
- **MANDATORY**: Adding any ADR requires GOV-ARCH-001 update in the same patch without exception.

## Safety Gate
- Do not delete or move files unless explicitly requested.
- Do not edit `./scripts/docs_verify.sh` or `./scripts/validate_schemas.sh` unless explicitly requested.
- If drift cleanup is requested, use deprecation stubs with canonical pointers by default.

## Validation Scripts Gate (Conditional)
- **During doc-generation runs**: When docs/** or contracts/** are modified, run and capture PASS output for both scripts before claiming completion:
  - `./scripts/docs_verify.sh`
  - `./scripts/validate_schemas.sh`
- **During skill-only edits**: Validation scripts are NOT required when only modifying the skill package (cloudrail-arch-docs/ directory). Skip script execution for skill-only changes.
- Execute MCP POST-FLIGHT calls per `references/mcp-validation.md`; update `MCP_EVIDENCE_LOG.md` with results and mark `UNVERIFIED EXTERNALLY` where tools unavailable.
