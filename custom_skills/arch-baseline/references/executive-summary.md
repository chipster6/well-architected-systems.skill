# Updated Executive Summary — arch-baseline

## Purpose

arch-baseline is a variance-reduction and governance bootstrapping skill. It establishes the project’s architectural baseline by:

1. locking documentation governance and golden templates
2. defining scope and baseline architecture boundaries
3. selecting the cloud provider (RFC → ADR)
4. executing post-decision research using MCP/web sources
5. normalizing findings into registries and policies
6. producing a Well-Architected Adherence Plan that governs downstream arch-docs

## Scope

### In scope
- Documentation governance standards and golden templates
- Canonical repo “truth locations” (docs/registries/audit)
- Provider selection and provider pack activation
- Post-decision research with auditable tool-call trail + evidence log
- Baseline C4 snapshot (Context + Container)
- Initialization (not full elaboration) of domain model and contract catalog
- Security baseline and operational readiness baseline sufficient to govern downstream docs

### Out of scope
- Full service-level architecture documentation (belongs to arch-docs)
- Full implementation planning and task orchestration (belongs to impl-strategy)
- Detailed contract specs and domain elaboration beyond baseline stubs

## Key outcome

After arch-baseline passes its gate, arch-docs can execute without re-asking foundational questions, because:
- “what to produce” is specified by governance + the adherence plan
- “what constraints apply” are in registries
- “what sources were used” is auditable (tool-call trail + evidence log)
- “where truth lives” is locked (paths, naming, IDs)
