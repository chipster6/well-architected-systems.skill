# Container View Notes

Primary containers within the Control Plane:

1. **Ingress/API Gateway** – Terminates client connections, enforces authentication, and forwards calls to service entrypoints. (AWS example: API Gateway + Lambda authorizers.)
2. **Command Orchestrator** – Coordinates long-running workflows and dispatches directives. (AWS example: ECS + Step Functions.)
3. **Telemetry Pipeline** – Captures telemetry, stores it durably, and routes signals to analytics/alerts. (AWS example: Kinesis + S3.)
4. **Rules Engine** – Evaluates guardrails, triggers mitigations, and records evidence. (AWS example: DynamoDB with point-in-time recovery.)
5. **Operations Portal** – UI for dashboards, playbooks, and approvals.

Inter-container contracts are documented in architecture documentation and reference shared schemas stored in the registries and contract catalog.
