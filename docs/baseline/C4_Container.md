# CloudRail Container View Notes

Primary containers within the CloudRail Control Plane:

1. **Ingress/API Gateway** – Terminates client connections, enforces authentication, and forwards calls to service mesh entrypoints. Runs on AWS API Gateway + Lambda authorizers.
2. **Command Orchestrator** – Coordinates routing plans and sends directives to fleets; implemented as an ECS service with Step Functions for long-running workflows.
3. **Telemetry Pipeline** – Kinesis streams capture train telemetry, store in S3/Lake Formation, and forward incidents to the analytics workspace.
4. **Safety Rules Engine** – Evaluates guardrails, halts trains when violations are detected, and records evidence in DynamoDB with point-in-time recovery enabled.
5. **Operations Portal** – React + Amplify application used by supervisors for dashboards, playbooks, and approvals.

Inter-container contracts are documented in the architecture RFCs and reference shared schemas stored in the service catalog.
