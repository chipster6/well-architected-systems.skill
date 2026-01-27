# Domain Model (Baseline Stub)

## Purpose
Provide a minimal shared vocabulary for the system so downstream documentation and task planning can use stable, unambiguous terms.

## Core concepts
- Asset: a managed item the system tracks (e.g., device, rail component, sensor).
- Telemetry: time-series measurements emitted by assets.
- Event: a discrete, time-bounded occurrence (e.g., alert, state transition).
- Policy: a rule that governs access or behavior (e.g., retention, authorization).

## Identifiers
- Assets and events should have stable IDs in registries and contracts when introduced.
- Naming conventions and ID formats must be consistent across documentation and schemas.

