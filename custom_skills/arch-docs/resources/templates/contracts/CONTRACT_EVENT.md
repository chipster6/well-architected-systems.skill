# Event Contract

## Purpose
- Define event structure, semantics, and delivery guarantees.

## Scope
- Producer: TOKEN_PRODUCER
- Consumers: TOKEN_CONSUMERS

## Event Schema
- Schema file: contracts/schemas/TOKEN_EVENT_SCHEMA
- Example: contracts/examples/TOKEN_EVENT_EXAMPLE

## Semantics
- Topic/Bus: TOKEN_TOPIC
- Delivery: TOKEN_DELIVERY (e.g., at-least-once)
- Ordering: TOKEN_ORDERING

## Security
- Tenant isolation: TOKEN_TENANT_ISOLATION
- Encryption: TOKEN_ENCRYPTION

## References
- MCP Evidence IDs: TOKEN_EVIDENCE_IDS
- Related ADRs: TOKEN_ADR_IDS

## Acceptance Criteria
- Schema and example validate.
- Delivery and ordering guarantees documented.
