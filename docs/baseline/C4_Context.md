# CloudRail Context Diagram Notes

The CloudRail platform interacts with three external actor groups:
1. **Rail Operations Supervisors** – manage safety overrides and review alerts.
2. **Autonomous Train Fleets** – publish telemetry and receive routing directives via MQTT over TLS.
3. **Third-Party Logistics Systems** – consume scheduling feeds through a hardened API gateway.

System boundaries:
- CloudRail Control Plane (this system) exposes APIs to actors and integrates with regional AWS services for compute, data, and observability.
- Legacy dispatch tooling is treated as an external dependency; integration occurs via message bus bridges documented in the architecture RFCs.
