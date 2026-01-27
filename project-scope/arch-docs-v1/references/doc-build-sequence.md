# Deterministic Documentation Build Sequence (Greenfield)

## Scope
This reference defines the mandatory build sequence for **greenfield documentation creation** in CloudRail architecture documentation. It ensures dependency order, contractual completeness, and governance compliance.

## Build Mode Declaration

**build_mode**: `greenfield` | `incremental`

- **greenfield**: New system/tenant/domain creation - MUST follow sequence A-G
- **incremental**: Existing system updates - may modify docs outside sequence but MUST validate impact

## Sequence Blocks A-G

### Block A - Product Foundations
**Documents in scope**:
- `docs/02_ARCHITECTURE/ARC-*.md` (System Architecture Overview)
- Business requirement documents
- High-level scope and boundary definitions

**Entry gates**:
- Project charter or equivalent exists
- Stakeholder approval received
- Geographic deployment region defined (default ca-central-1)

**Exit gates**:
- System boundaries and trust zones clearly defined
- Control Plane vs Tenant Plane separation established
- GOV-ARCH-001 updated with new ARC references

**Mandatory index updates**:
- GOV-ARCH-001: Add ARC entries to Architecture Index

### Block B - Architecture + ADR
**Documents in scope**:
- `docs/09_GOVERNANCE/ADR-*.md` (Architecture Decision Records)
- Detailed technical specifications
- Integration patterns and external dependencies

**Entry gates**:
- Block A artifacts complete and approved
- System architecture review conducted
- Technology stack decisions finalized

**Exit gates**:
- All major architectural decisions recorded with ADRs
- MCP evidence attached for technical claims (MCP-YYYYMMDD-NNNN)
- Cross-cutting concerns addressed (security, performance, reliability)

**Mandatory index updates**:
- GOV-ARCH-001: Add ADR entries to Decision Index
- REGISTRY: Update service dependencies if applicable

### Block C - Contracts
**Documents in scope**:
- `docs/03_CONTRACTS/DM-*.md` (Data Model specifications)
- `contracts/schemas/*.schema.json` (JSON schemas)
- `contracts/examples/**/*` (Schema validation examples)
- API contracts and interface definitions

**Entry gates**:
- Blocks A-B artifacts complete
- Data model requirements finalized
- Interface specifications approved

**Exit gates**:
- All schemas have corresponding examples that validate
- Schema versioning strategy established
- Contract-first validation passes (`./scripts/validate_schemas.sh`)
- Documentation hygiene passes (`./scripts/docs_verify.sh`)

**Mandatory index updates**:
- REGISTRY: Add all new contracts and schemas
- GOV-ARCH-001: Add DM entries to Model Index

### Block D - Services
**Documents in scope**:
- `docs/04_SERVICES/SERVICE_*.md` (Service specifications)
- Service-level architecture and responsibility boundaries
- Internal/external service interfaces

**Entry gates**:
- Blocks A-C artifacts complete
- Service contracts finalized
- Service ownership assigned

**Exit gates**:
- Service boundaries clearly defined
- Service dependencies documented
- Interface contracts reference Block C schemas
- Error handling and retry strategies defined

**Mandatory index updates**:
- GOV-ARCH-001: Add SERVICE entries to Service Index
- REGISTRY: Update service registry with dependencies

### Block E - Workflows
**Documents in scope**:
- `docs/05_WORKFLOWS/WORKFLOW_*.md` (Workflow specifications)
- `docs/05_WORKFLOWS/RUNNER_CONTRACT.md` (Runner interface)
- Process orchestration and step function definitions

**Entry gates**:
- Blocks A-D artifacts complete
- Workflow requirements documented
- Service dependencies identified

**Exit gates**:
- Workflow orchestrators defined with Step Functions
- Runner contracts established for tenant isolation
- Error handling and compensation patterns documented
- Workflow observability and logging defined

**Mandatory index updates**:
- GOV-ARCH-001: Add WORKFLOW entries to Workflow Index

### Block F - Datastores
**Documents in scope**:
- Data persistence specifications
- Database schemas and migration strategies
- Data lifecycle and retention policies
- Backup and disaster recovery procedures

**Entry gates**:
- Blocks A-E artifacts complete
- Data model from Block C approved
- Storage requirements finalized

**Exit gates**:
- Persistence layer implementation defined
- Data encryption and access controls specified
- Consistency and isolation guarantees documented
- Multi-tenant data isolation established

**Mandatory index updates**:
- GOV-ARCH-001: Update Data Model Index with persistence details
- REGISTRY: Add datastore dependencies

### Block G - Security/Ops/Implementation
**Documents in scope**:
- `docs/06_SECURITY/*.md` (Security controls)
- `docs/07_OPERATIONS/*.md` (Operational procedures)
- `docs/08_IMPLEMENTATION/*.md` (Implementation guides)
- Monitoring, alerting, and incident response

**Entry gates**:
- Blocks A-F artifacts complete
- Security requirements finalized
- Operational readiness criteria defined

**Exit gates**:
- Security posture assessment complete
- Monitoring and alerting configured
- Deployment and maintenance procedures documented
- Incident response playbooks established
- All evidence tokens replaced with concrete evidence

**Mandatory index updates**:
- GOV-ARCH-001: Add security, operations, and implementation entries
- Final REGISTRY synchronization

## Deviation Policy (Waiver Process)

### Waiver Triggers
A WAIVER is required when:
1. **Out-of-sequence creation**: Producing docs from a future block (e.g., creating Service docs in Block B)
2. **Parallel block work**: Simultaneously working across multiple blocks without proper dependencies
3. **Block skipping**: Attempting to bypass a required sequence block

### Waiver Requirements
Every WAIVER must include in the phase completion report:

**rationale**: 
- Business or technical justification for deviation
- Why the standard sequence cannot be followed
- Risk assessment of the deviation

**impacted dependencies**:
- List of specific dependencies that will be affected
- Downstream impacts on other sequence blocks
- Validation gaps created by the deviation

**backfill plan**:
- Specific actions to restore canonical ordering
- Timeline for completing backfilled requirements
- Validation steps to ensure dependency satisfaction

### Waiver Validation
- WAIVER must be explicitly approved in the phase completion report
- Backfill plan must have concrete dates and owners
- Subsequent phases must validate WAIVER completion before proceeding

## Enforcement

### Quality Gate Integration
The DOC_SEQUENCE_GATE in quality-gates.md validates:
1. build_mode declaration presence
2. sequence_block compliance for greenfield mode
3. WAIVER presence and completeness when required

### Mechanical Validation
- Phase completion reports must declare build_mode and sequence_block
- Greenfield runs without sequence compliance must include WAIVER
- All mechanical checks (docs_verify.sh, validate_schemas.sh) must pass

## Usage

### Starting a Greenfield Build
1. Declare build_mode=greenfield in P0
2. Select sequence_block=A in P0
3. Follow Block A entry/exit gates
4. Progress to Block B only after Block A exit gates satisfied
5. Continue sequentially through Block G

### Incremental Updates
1. Declare build_mode=incremental in P0
2. May modify docs across multiple blocks
3. Must validate impact on dependent artifacts
4. No WAIVER required but impact analysis mandatory