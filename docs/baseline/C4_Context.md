# Context Diagram Notes

The system interacts with three external actor groups:
1. **Operations users** – manage safety overrides and review alerts.
2. **Connected assets/devices** – publish telemetry and receive directives via authenticated channels.
3. **Third-party systems** – consume or publish data through a hardened API boundary.

System boundaries:
- Control Plane (this system) exposes APIs to actors and integrates with regional AWS services for compute, data, and observability (per ADR).
- Any legacy tooling is treated as an external dependency; integration occurs via documented bridges and contracts.
