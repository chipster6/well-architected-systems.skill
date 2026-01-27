# API Contract

## Purpose
- Define the REST/HTTP interface, payloads, and guarantees.

## Scope
- Service: TOKEN_SERVICE
- Audience: TOKEN_AUDIENCE

## Endpoints
| Method | Path | Description | Auth | Idempotency |
|--------|------|-------------|------|-------------|
| TOKEN_METHOD | TOKEN_PATH | TOKEN_DESC | TOKEN_AUTH | TOKEN_IDEMP |

## Request Schema
- Schema file: contracts/schemas/TOKEN_REQUEST_SCHEMA
- Example: contracts/examples/TOKEN_REQUEST_EXAMPLE

## Response Schema
- Schema file: contracts/schemas/TOKEN_RESPONSE_SCHEMA
- Example: contracts/examples/TOKEN_RESPONSE_EXAMPLE

## Error Model
- Follows RFC 7807 Problem Details.

## Security
- AuthZ: TOKEN_AUTHZ
- Region default ca-central-1; tenant isolation enforced via AssumeRole external ID.

## References
- MCP Evidence IDs: TOKEN_EVIDENCE_IDS
- Related ADRs: TOKEN_ADR_IDS

## Acceptance Criteria
- Schemas and examples validate.
- Auth, rate limits, and idempotency defined.
