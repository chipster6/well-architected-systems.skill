# Runner Contract

## Purpose
- Define expectations for runners executing workflow tasks.

## Scope
- Runner type: TOKEN_RUNNER_TYPE

## Interface
- Inputs: TOKEN_INPUTS
- Outputs: TOKEN_OUTPUTS
- Idempotency: TOKEN_IDEMPOTENCY

## Security
- AssumeRole with external ID; permission boundary ARN: TOKEN_PERMISSION_BOUNDARY
- Network: TOKEN_NETWORK

## Observability
- Logs/metrics/traces: TOKEN_OBS

## References
- MCP Evidence IDs: TOKEN_EVIDENCE_IDS
- Related ADRs: TOKEN_ADR_IDS

## Acceptance Criteria
- Contract aligns with workflow spec triggers and retries.
- Security and observability fields are complete.
