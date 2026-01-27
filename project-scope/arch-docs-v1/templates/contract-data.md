# Data Contract

## Purpose
- Define data model exchange for storage or batch interfaces.

## Scope
- Producer/Owner: TOKEN_OWNER
- Consumers: TOKEN_CONSUMERS

## Schema
- Schema file: contracts/schemas/TOKEN_SCHEMA
- Example: contracts/examples/TOKEN_EXAMPLE

## Fields
| Name | Type | Required | Description | Constraints |
|------|------|----------|-------------|-------------|
| TOKEN_FIELD | TOKEN_TYPE | TOKEN_REQUIRED | TOKEN_DESC | TOKEN_CONSTRAINT |

## Versioning
- Current version: TOKEN_VERSION
- Breaking change policy: TOKEN_BREAKING_POLICY

## Security & Residency
- Region default ca-central-1 unless contractually overridden.
- Encryption: TOKEN_ENCRYPTION
- PII classification: TOKEN_PII

## References
- MCP Evidence IDs: TOKEN_EVIDENCE_IDS
- Related ADRs: TOKEN_ADR_IDS

## Acceptance Criteria
- Schema validates against examples.
- Versioning and residency rules documented.
