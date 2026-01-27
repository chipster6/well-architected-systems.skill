# Phase PHASE_NUMBER Completion Report (PHASE_COMPLETION_REPORT_PN)

Date: TOKEN_DATE_ISO
Doc: TOKEN_DOC_PATH

## Build Configuration
- **build_mode**: TOKEN_BUILD_MODE (greenfield|incremental)
- **sequence_block**: TOKEN_SEQUENCE_BLOCK (A|B|C|D|E|F|G, required if greenfield)
- **sequence_compliance**: TOKEN_SEQUENCE_COMPLIANCE (compliant|waiver)

## What was completed
- TOKEN_COMPLETED

## Evidence
- MCP Evidence IDs used: TOKEN_EVIDENCE_IDS
- WELL_ARCHITECTED_PILLAR_MATRIX updates: TOKEN_WA_UPDATES

## References
- MCP Evidence IDs used: TOKEN_EVIDENCE_IDS
- Related ADRs: TOKEN_ADR_IDS

## Sequence Waiver (required if sequence_compliance=waiver)
### Rationale
TOKEN_WAIVER_RATIONALE

### Impacted Dependencies
TOKEN_WAIVER_IMPACTED_DEPS

### Backfill Plan
TOKEN_WAIVER_BACKFILL_PLAN

## Blockers (if any)
- TOKEN_BLOCKERS

## Sign-off
- Prepared by: TOKEN_PREPARED_BY
- Reviewed by: TOKEN_REVIEWED_BY

## File Naming Convention
This file must be named following the pattern: PHASE_COMPLETION_REPORT_PN.md where N is the phase number (0-6).
