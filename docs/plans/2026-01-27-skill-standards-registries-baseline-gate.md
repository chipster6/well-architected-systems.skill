# Skill Standards + Registries + Baseline Gate Hardening Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Make `arch-docs` and `impl-strategy` SKILL.md files conform to repo skill standards, populate baseline registries with at least one stable-ID entry each, and harden the baseline gate to enforce `baseline_manifest.json` mandatory artifacts (while keeping gates green).

**Architecture:** This is a docs-and-validator alignment pass. We (1) add YAML frontmatter + discovery-grade triggers + progressive disclosure links in the two skill entrypoints, (2) treat registries as normalized system-of-record by adding minimal structured entries, and (3) update the baseline validator to enforce the baseline manifest contract (mandatory artifacts + optional non-empty registry enforcement). Since hardening will surface currently-missing mandatory artifacts, we will create those baseline artifacts so the baseline gate still passes after the validator change.

**Tech Stack:** Markdown, YAML, Python (baseline validator), shell wrapper scripts.

## Preconditions / Notes
- There is no `superpowers:plan` skill available in this environment; the closest match is `superpowers:writing-plans`, which produced this plan.
- Gate wrappers to use as success criteria:
  - `./tools/run_baseline_gate.sh`
  - `./tools/run_arch_docs_gate.sh`
  - `./tools/run_impl_gate.sh`

## Current repo status snapshot (2026-01-27)
- Completed (already merged to `origin/main`):
  - arch-docs + impl-strategy reference docs exist under `custom_skills/*/references/`
  - arch-docs + impl-strategy policy YAMLs required by current validators are non-empty
  - `docs/architecture/` and `docs/implementation/` exist (tracked via `.gitkeep`)
  - Wrapper gates currently PASS (but are still shallow).
- Not yet done (this plan covers):
  - YAML frontmatter (name/version/description w/ explicit triggers) for:
    - `custom_skills/arch-docs/SKILL.md`
    - `custom_skills/impl-strategy/SKILL.md`
  - Registries are currently empty (all `registries/*.yml` are 0 bytes).
  - Baseline gate hardening is not yet implemented; `validate_baseline.py` does not enforce `baseline_manifest.json["artifacts"]`.
  - `baseline_manifest.json` currently marks multiple mandatory artifacts that do not exist yet (docs governance, ADR policy, golden templates dir, etc.).

## Smallest executable next action (tight feedback loop)
Before making further changes, run these now to confirm current baseline state:

Run:
`./tools/run_arch_docs_gate.sh`
Expected: PASS (exit 0).

Run:
`./tools/run_impl_gate.sh`
Expected: PASS (exit 0).

Note: After Task 5 (baseline gate hardening), baseline gate is expected to FAIL until Task 6 creates missing mandatory artifacts.

### Task 1: Inspect current SKILL.md files (arch-docs, impl-strategy)

**Files:**
- Modify: none

**Step 1: Open current skill entrypoints**

Run:
`sed -n '1,120p' custom_skills/arch-docs/SKILL.md && echo '---' && sed -n '1,120p' custom_skills/impl-strategy/SKILL.md`

Expected: No YAML frontmatter currently; confirm where to insert it.

### Task 2: Add YAML frontmatter + discovery-grade triggers + progressive disclosure links (arch-docs)

**Files:**
- Modify: `custom_skills/arch-docs/SKILL.md`

**Step 1: Add YAML frontmatter at top of file**

Insert at the very top:

```yaml
---
name: arch-docs
version: "1.0"
description: >
  Use when you need to generate, expand, validate, or govern architecture documentation (C4, service specs, security architecture, threat model, operations model, contracts) from an established baseline.
  Triggers: "architecture docs", "C4 component", "service catalog", "threat model", "security architecture", "operations/runbook", "contract spec", "well-architected mapping", "arch-docs gate", "validate_docs.py".
  Requires baseline gate PASS; fails closed on missing required policy inputs and docs/architecture/.
---
```

**Step 2: Add progressive disclosure links near the top of the body**

Add a small section (near top, after H1) linking to:
- `custom_skills/arch-docs/references/executive-summary.md`
- `custom_skills/arch-docs/references/ARCH_DOCS_PHASES.md`

Example snippet:

```md
## References (progressive disclosure)
- `references/executive-summary.md`
- `references/ARCH_DOCS_PHASES.md`
```

**Step 3: Validate the file starts with YAML frontmatter**

Run: `head -n 20 custom_skills/arch-docs/SKILL.md`
Expected: YAML frontmatter present; includes explicit triggers.

### Task 3: Add YAML frontmatter + discovery-grade triggers + progressive disclosure links (impl-strategy)

**Files:**
- Modify: `custom_skills/impl-strategy/SKILL.md`

**Step 1: Add YAML frontmatter at top of file**

Insert at the very top:

```yaml
---
name: impl-strategy
version: "1.0"
description: >
  Use when you need to turn baseline + architecture documentation into an executable implementation strategy: phased plan, dependency DAG (TASK_DAG.json), task catalog, and optional worktree/parallelization plan.
  Triggers: "implementation strategy", "task dag", "dependency graph", "milestones", "phase plan", "worktree plan", "impl gate", "validate_task_graph.py".
  Requires baseline gate PASS and docs/implementation/; fails closed if required policy inputs are missing.
---
```

**Step 2: Add progressive disclosure links near the top of the body**

Add links to:
- `custom_skills/impl-strategy/references/executive-summary.md`
- `custom_skills/impl-strategy/references/IMPL_STRATEGY_PHASES.md`

**Step 3: Validate the file starts with YAML frontmatter**

Run: `head -n 20 custom_skills/impl-strategy/SKILL.md`
Expected: YAML frontmatter present; includes explicit triggers.

### Task 4: Populate required registries with minimal stable-ID entries (and recommended catalogs)

**Files:**
- Modify: `registries/constraints_registry.yml`
- Modify: `registries/security_controls_catalog.yml`
- Modify: `registries/slo_catalog.yml`
- Modify (recommended): `registries/service_catalog.yml`
- Modify (recommended): `registries/event_catalog.yml`
- Modify (recommended): `registries/env_catalog.yml`

**Step 1: Add minimal structured YAML to each file (no placeholders)**

Use these minimal schemas (adjust values to match current baseline scope/provider as needed; stable IDs must not change without an ADR):

`registries/constraints_registry.yml`
```yaml
version: 1
constraints:
  - id: "CONSTRAINT-0001"
    title: "Baseline-first governance"
    statement: "Downstream skills must not proceed unless the baseline gate passes."
    scope: "repo"
    rationale: "Enforces deterministic, auditable architecture work."
    source: "docs/baseline/BASELINE_HANDOFF.md"
    owner_role: "architecture"
    status: "active"
```

`registries/security_controls_catalog.yml`
```yaml
version: 1
controls:
  - id: "SECCTRL-0001"
    title: "Least privilege access"
    objective: "Ensure identities only have permissions required for their role."
    scope: "system"
    implementation_notes: "Define roles and access boundaries; review privileges periodically."
    verification: "Access review evidence and automated policy checks where available."
    owner_role: "security"
    status: "active"
```

`registries/slo_catalog.yml`
```yaml
version: 1
slos:
  - id: "SLO-0001"
    service_id: "SERVICE-0001"
    name: "API availability"
    sli: "successful_requests / total_requests"
    target: "99.9%"
    window: "30d"
    measurement: "server-side metrics"
    owner_role: "sre"
    status: "active"
```

Recommended catalogs (minimal entries):

`registries/service_catalog.yml`
```yaml
version: 1
services:
  - id: "SERVICE-0001"
    name: "core-api"
    type: "service"
    description: "Primary API boundary for the system."
    owner_role: "engineering"
    status: "active"
```

`registries/event_catalog.yml`
```yaml
version: 1
events: []
```

`registries/env_catalog.yml`
```yaml
version: 1
environments:
  - id: "ENV-0001"
    name: "dev"
    purpose: "Development environment"
    status: "active"
```

**Step 2: Validate YAML parses for all registries**

Run:
`python3 - <<'PY'\nfrom pathlib import Path\ntry:\n  import yaml  # type: ignore\nexcept Exception as exc:\n  raise SystemExit(f\"PyYAML not available: {exc}\")\npaths=[\n  'registries/constraints_registry.yml',\n  'registries/security_controls_catalog.yml',\n  'registries/slo_catalog.yml',\n  'registries/service_catalog.yml',\n  'registries/event_catalog.yml',\n  'registries/env_catalog.yml',\n]\nfor p in paths:\n  data=yaml.safe_load(Path(p).read_text())\n  assert data is not None, p\nprint('YAML OK')\nPY`

Expected: `YAML OK`

Fallback (if PyYAML is not available): `ruby -ryaml -e 'ARGV.each{|p| YAML.load_file(p) or raise p}; puts \"YAML OK\"' registries/*.yml`

### Task 5: Harden baseline gate to enforce baseline_manifest.json mandatory artifacts

**Files:**
- Modify: `custom_skills/arch-baseline/scripts/validate_baseline.py`

**Step 1: Add manifest artifacts enforcement**

Implement logic:
- Load `docs/baseline/baseline_manifest.json`
- Iterate `manifest["artifacts"]`
- For each `mandatory: true`:
  - If `type == "directory"`: require `Path(path).is_dir()`
  - Else: require `Path(path).exists()`
- Fail with a numbered list of missing mandatory artifacts if any are missing

**Step 2: Optionally enforce non-empty registries**

For each `manifest["registries"]` entry where `mandatory: true`:
- Fail if file missing
- Fail if file is empty OR parses but contains zero entries (fail-closed)

**Step 3: Verify baseline gate now fails when a mandatory artifact is missing**

To avoid destructive changes, verify by pointing the check at the current known-missing list:
- Run: `./tools/run_baseline_gate.sh`
Expected (before creating missing artifacts): FAIL and list missing mandatory artifacts from the manifest.

### Task 6: Create missing mandatory baseline artifacts (to restore baseline gate PASS)

**Files:**
- Create: `docs/baseline/DOCS_GOVERNANCE.md`
- Create: `docs/baseline/ADR_POLICY.md`
- Create: `docs/baseline/golden_templates/.gitkeep`
- Create: `docs/baseline/SCOPE_BOUNDARIES.md`
- Create: `docs/baseline/PROVIDER_COMPARISON_RFC.md`
- Create: `docs/baseline/TOOLCHAIN_BASELINE.md`
- Create: `docs/baseline/DOMAIN_MODEL.md`
- Create: `docs/baseline/CONTRACT_CATALOG.md`
- Create: `docs/baseline/SECURITY_BASELINE.md`
- Create: `docs/baseline/OPS_READINESS_STANDARD.md`

**Step 1: Create each missing doc with minimal, concrete content**

No TODO/TBD placeholders. Each file must have an H1 and a small set of sections consistent with the repo’s governance expectations.

**Step 2: Re-run baseline gate**

Run: `./tools/run_baseline_gate.sh`
Expected: PASS.

### Task 7: Final verification (all gates)

**Files:**
- Modify: none

**Step 1: Run all wrappers**

Run:
`./tools/run_baseline_gate.sh && ./tools/run_arch_docs_gate.sh && ./tools/run_impl_gate.sh`

Expected: all PASS (exit 0).

### Task 8: Commit + push (keep changes logically separated)

**Files:**
- Modify/Create: as above

**Step 1: Commit SKILL.md frontmatter changes**

Run:
`git add custom_skills/arch-docs/SKILL.md custom_skills/impl-strategy/SKILL.md`

Then:
`git commit -m "docs: add skill frontmatter + references links"`

**Step 2: Commit registry population**

Run:
`git add registries/*.yml`

Then:
`git commit -m "chore: populate canonical registries (minimal entries)"`

**Step 3: Commit baseline gate hardening + missing artifacts**

Run:
`git add custom_skills/arch-baseline/scripts/validate_baseline.py docs/baseline/*.md docs/baseline/golden_templates/.gitkeep`

Then:
`git commit -m "chore: enforce baseline manifest artifacts in baseline gate"`

**Step 4: Push**

Run: `git push origin main`
Expected: remote updated; CI enforces the hardened baseline contract.

### Task 9: Implement the “real machinery” (arch-docs + impl-strategy scripts + schemas)

**Files:**
- Modify (arch-docs scripts, currently empty):
  - `custom_skills/arch-docs/scripts/scaffold_docs.py`
  - `custom_skills/arch-docs/scripts/emit_audit_bundle.py`
  - `custom_skills/arch-docs/scripts/update_indexes.py`
  - `custom_skills/arch-docs/scripts/utils_frontmatter.py`
- Modify (arch-docs schemas, currently empty):
  - `custom_skills/arch-docs/resources/schemas/audit_bundle.schema.json`
  - `custom_skills/arch-docs/resources/schemas/claim_index.schema.json`
  - `custom_skills/arch-docs/resources/schemas/doc_manifest.schema.json`
- Modify (impl-strategy scripts, currently empty):
  - `custom_skills/impl-strategy/scripts/build_task_graph.py`
  - `custom_skills/impl-strategy/scripts/decompose_phases.py`
  - `custom_skills/impl-strategy/scripts/plan_worktrees.py`
  - `custom_skills/impl-strategy/scripts/emit_delivery_bundle.py`
- Modify (impl-strategy schemas, currently empty):
  - `custom_skills/impl-strategy/resources/schemas/task_graph.schema.json`
  - `custom_skills/impl-strategy/resources/schemas/phase_plan.schema.json`
  - `custom_skills/impl-strategy/resources/schemas/worktree_manifest.schema.json`
  - `custom_skills/impl-strategy/resources/schemas/gate_results.schema.json`
- Modify (validators should start checking content, not just “non-empty”):
  - `custom_skills/arch-docs/scripts/validate_docs.py`
  - `custom_skills/impl-strategy/scripts/validate_task_graph.py`

**Step 1: arch-docs scaffold (generate minimal docs from baseline manifest + templates)**

Implement `scaffold_docs.py` to:
- read `docs/baseline/baseline_manifest.json` for canonical paths
- create a deterministic run id `RUN-YYYYMMDD-HHMM-arch-docs-scaffold`
- create `docs/architecture/` docs if missing
- render minimal doc set (even if templates are sparse) and write:
  - `docs/architecture/ARC_OVERVIEW.md`
  - `docs/architecture/SERVICE_CATALOG.md`
  - `docs/architecture/SECURITY_ARCHITECTURE.md`
  - `docs/architecture/THREAT_MODEL.md`
  - `docs/architecture/OPERATIONS_MODEL.md`
  - `docs/architecture/WELL_ARCHITECTED_PILLAR_MATRIX.md`

Run: `python3 custom_skills/arch-docs/scripts/scaffold_docs.py`
Expected: files created/updated deterministically.

**Step 2: arch-docs audit bundle + indexes**

Implement:
- `emit_audit_bundle.py` to write `docs/audit/arch-docs/<run-id>/` artifacts required by repo AGENTS.md
- `update_indexes.py` to update any inventory/index docs (e.g., `docs/architecture/ARCHITECTURE_INDEX.md`) deterministically

Run: `python3 custom_skills/arch-docs/scripts/emit_audit_bundle.py --run-id <run-id>`
Expected: run folder created with required files.

**Step 3: impl-strategy DAG + phase plan**

Implement:
- `build_task_graph.py` to generate `docs/implementation/TASK_DAG.json` from baseline + arch-docs outputs (service catalog, decisions, etc.)
- `decompose_phases.py` to generate `docs/implementation/PHASE_PLAN.md` from the DAG
- `plan_worktrees.py` (optional) to generate `docs/implementation/WORKTREE_PLAN.md`
- `emit_delivery_bundle.py` to write `docs/audit/impl-strategy/<run-id>/` artifacts required by repo AGENTS.md

Run: `python3 custom_skills/impl-strategy/scripts/build_task_graph.py`
Expected: `docs/implementation/TASK_DAG.json` exists and is valid JSON.

**Step 4: Fill schemas and validate outputs against them**

Fill the JSON Schema files and have scripts validate outputs:
- arch-docs: claim index / audit bundle / doc manifest schemas
- impl-strategy: task graph / phase plan / worktree manifest / gate results schemas

Run: `python3 -c 'import json; json.load(open(\"docs/implementation/TASK_DAG.json\"))'`
Expected: exit 0.

**Step 5: Upgrade validators to check content (not just existence)**

Update validators to fail closed unless:
- arch-docs: expected doc files exist and have non-trivial content (e.g., > N bytes) AND required baseline crosslinks exist
- impl-strategy: `TASK_DAG.json` exists, is valid JSON, is acyclic, and tasks include required fields

**Step 6: End-to-end success check**

Run:
`./tools/run_baseline_gate.sh && ./tools/run_arch_docs_gate.sh && ./tools/run_impl_gate.sh`

Expected:
- baseline PASS
- arch-docs PASS and scaffold produces docs
- impl-strategy PASS and produces valid DAG
