# Provider Packs v1 Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Make provider packs the single mechanism for cloud-specific baseline behavior: generate the Well-Architected adherence plan post-decision, populate baseline registries, and extend validation rules so the baseline gate can fail-closed without hardcoded provider assumptions.

**Architecture:** A provider pack is a machine-consumable directory under `custom_skills/arch-baseline/resources/provider_packs/{aws|azure|gcp}/` containing structured YAML files (pillars, controls, constraints, validation rules, sources/recency, and optional toolchain overlays). The baseline workflow loads the chosen provider pack after the provider decision ADR, materializes provider-specific mappings into the adherence plan + registries, and activates provider-aware validation extensions.

**Tech Stack:** Python validators/scripts, YAML pack files, JSON Schema (optional), existing baseline gate wrappers.

## Step 0: Verify repo context (must do before edits)

This plan is authored for the **well-architected-systems skill repo**. The repo root may not be named "cloudrail-system".

Run and paste results into the terminal output:
- `pwd`
- `git rev-parse --show-toplevel`
- `ls -la docs/plans`
- `ls -la custom_skills/arch-baseline/resources || true`
- `ls -la custom_skills/arch-baseline/resources/provider_packs || true`

If `docs/plans/2026-01-27-provider-packs-v1.md` does not exist: STOP and print a clear error.

## Known Gaps / Required Fixes (Must Address)

These must be addressed as part of this plan. Do not proceed to downstream tasks until A/B/C are satisfied with explicit acceptance tests and negative tests.

### A) Validator invocation + fail-closed behavior

**Requirement**
- `custom_skills/arch-baseline/scripts/validate_provider_pack.py` exists and returns non-zero on any pack structure/schema failure.
- `custom_skills/arch-baseline/scripts/validate_baseline.py` invokes the provider pack validator when provider != `unselected` (directly or by importing/calling its entrypoint).
- `tools/run_baseline_gate.sh` propagates non-zero exit codes from baseline validation (no swallowing failures).

**Acceptance tests**
1) Provider selected + pack missing => baseline gate FAILS
- Command (example, aws):
  - Edit `docs/baseline/WELL_ARCHITECTED_ADHERENCE_PLAN.md` frontmatter to set `provider: aws`
  - Temporarily move pack dir out of the way:
    - `mv custom_skills/arch-baseline/resources/provider_packs/aws /tmp/provider_pack_aws.bak`
  - Run: `./tools/run_baseline_gate.sh`
  - Expected: exit code `1` and output contains an error string like:
    - `Missing provider pack directory: custom_skills/arch-baseline/resources/provider_packs/aws`
  - Restore: `mv /tmp/provider_pack_aws.bak custom_skills/arch-baseline/resources/provider_packs/aws`
2) Pack file violates schema => validate_provider_pack FAILS (non-zero)
- Command:
  - Introduce a deterministic schema violation (example): remove a required key from `custom_skills/arch-baseline/resources/provider_packs/aws/pack.yml` (e.g., delete `provider:` line)
  - Run: `python3 custom_skills/arch-baseline/scripts/validate_provider_pack.py --provider aws`
  - Expected: exit code `1` and output contains an error string like:
    - `pack.yml: missing required key: provider`

**Negative tests**
- `python3 custom_skills/arch-baseline/scripts/validate_provider_pack.py --provider does-not-exist`
  - Expected: exit code `2` and output contains:
    - `Unknown provider: does-not-exist`
- `python3 custom_skills/arch-baseline/scripts/validate_provider_pack.py --provider aws` when any required file is missing
  - Expected: exit code `1` and output contains:
    - `Missing required file: <path>`

### B) Path mismatch correction

**Requirement**
- All plan steps must reference the actual pack location:
  - `custom_skills/arch-baseline/resources/provider_packs/{aws,azure,gcp}/`

**Acceptance criterion**
- No plan steps reference the old path; grep confirms zero hits.
- Command (string assembled to avoid embedding the deprecated path in this plan file):
  - `OLD_PATH=\"$(printf '%s%s' 'resources/templates/' 'provider_packs')\"; grep -R \"$OLD_PATH\" -n docs/plans/2026-01-27-provider-packs-v1.md`
  - Expected: no matches (exit code `1`).

### C) Template-mode guardrail

**Requirement**
- Template-mode PASS is allowed ONLY when `provider == unselected`.
- If `provider != unselected` (i.e., `aws|azure|gcp`), then baseline gate MUST fail-closed until:
  - the selected provider pack exists, and
  - the provider pack validator returns exit code 0, and
  - provider-specific validation rules are enforced.

**Acceptance test**
- Set `provider: aws` in `docs/baseline/WELL_ARCHITECTED_ADHERENCE_PLAN.md` and run:
  - `./tools/run_baseline_gate.sh`
  - Expected: exit code `1` until the aws pack exists AND validates.

**Enforcement requirement**
- `custom_skills/arch-baseline/scripts/validate_baseline.py` must enforce this rule (not just documentation).

## Task 1: Freeze the pack interface (schema + file layout)

**Files:**
- Create: `custom_skills/arch-baseline/resources/schemas/provider_pack.schema.json`
- Create: `custom_skills/arch-baseline/resources/schemas/services.schema.json`
- Create: `custom_skills/arch-baseline/resources/provider_packs/_templates/pack.template.yml`
- Create: `custom_skills/arch-baseline/resources/provider_packs/_templates/pillars.template.yml`
- Create: `custom_skills/arch-baseline/resources/provider_packs/_templates/controls.template.yml`
- Create: `custom_skills/arch-baseline/resources/provider_packs/_templates/constraints.template.yml`
- Create: `custom_skills/arch-baseline/resources/provider_packs/_templates/validation_rules.template.yml`
- Create: `custom_skills/arch-baseline/resources/provider_packs/_templates/sources.template.yml`
- Create: `custom_skills/arch-baseline/resources/provider_packs/_templates/services.taxonomy.template.yml`
- Create: `custom_skills/arch-baseline/resources/provider_packs/_templates/services.core.template.yml`
- Create: `custom_skills/arch-baseline/resources/provider_packs/_templates/services.full.template.yml`
- Create: `custom_skills/arch-baseline/resources/provider_packs/_templates/overlays.kubernetes.template.yml`
- Create: `custom_skills/arch-baseline/resources/provider_packs/_templates/overlays.terraform.template.yml`
- Create: `custom_skills/arch-baseline/resources/provider_packs/_templates/overlays.cdk.template.yml`
- Create: `custom_skills/arch-baseline/scripts/validate_provider_pack.py`

**Step 1: Decide v1 file structure (multi-file pack)**

Pack directory layout (enforced):
```
custom_skills/arch-baseline/resources/provider_packs/<provider>/
  pack.yml
  pillars.yml
  controls.yml
  constraints.yml
  validation_rules.yml
  sources.yml
  services/
    taxonomy.yml
    services_core.yml
    services_full.yml   # optional (generated)
  overlays/
    kubernetes.yml   # optional
    terraform.yml    # optional
    cdk.yml          # optional
```

**Step 2: Define provider_pack.schema.json (fail-closed completeness)**

Schema (at minimum) should assert:
- required files exist (pack.yml required; others required by validator even if schema can’t enforce multi-file)
- pack metadata has: provider, version, reviewed_at, recency_days, pillar_ids
- pillars.yml includes: canonical pillar ids/names, review defaults, required evidence types per pillar, waiver defaults
- controls.yml includes: normalized control entries with fields:
  - control_id, category, provider_reference, required_for, evidence_required, normalization_target
- services/taxonomy.yml defines the taxonomy (categories + required subcategories)
- services/services_core.yml includes curated core provider service catalog entries and meets minimum category coverage checks
- services/services_full.yml rules are enforced only when enabled by pack policy (see Task 3)
- constraints.yml includes: naming + structural constraints and environment taxonomy
- validation_rules.yml includes: required artifacts, registry field requirements, crosslink rules, toolchain applicability checks
- sources.yml includes: authoritative sources, topic→evidence mapping, recency policy

**Step 3: Add pack templates (aligned to actual pack location)**

Create templates mirroring v1 structure under:
- `custom_skills/arch-baseline/resources/provider_packs/_templates/`

**Step 4: Add a pack linter script (fail-closed)**

- Validate:
  - directory exists for aws/azure/gcp
  - required files present
  - YAML loads (stdlib-only if possible; otherwise vendor a minimal parser or enforce conservative structural checks)
  - minimum required keys exist and lists are non-empty
  - services taxonomy exists and meets mandatory category requirements (see Task 3)
  - services_core exists, validates, and meets core coverage requirements (see Task 3)
  - services_full is optional but must validate when present and enabled (see Task 3)

Run: `python3 custom_skills/arch-baseline/scripts/validate_provider_pack.py --provider aws`
Expected: PASS (exit 0) once packs are filled.
Negative test: delete one required file and re-run; Expected: FAIL (exit 1) with `Missing required file: ...`.

## Task 2: Implement template-mode vs post-decision mode in adherence plan validator

**Files:**
- Modify: `custom_skills/arch-baseline/scripts/validate_well_architected.py`
- Modify: `docs/baseline/WELL_ARCHITECTED_ADHERENCE_PLAN.md`

**Step 1: Template-mode (provider: unselected)**

Validator must require a different heading set, including:
- provider selection procedure (RFC + ADR references)
- provider pack reference section (pack paths)
- a placeholder-free statement explaining how pillar mapping is materialized post-decision

**Step 2: Post-decision mode (provider in aws/azure/gcp)**

Validator must require:
- pillar mapping table present and non-empty
- pillar set matches the chosen provider pack (canonical pillar ids/names)
- evidence requirements are referenced and traceable

Run: `./tools/run_baseline_gate.sh`
Expected: PASS in template-mode for this repo’s baseline scaffolding.

## Task 3: Standardize provider packs (AWS/Azure/GCP) to v1

**Files:**
- Modify/Create: `custom_skills/arch-baseline/resources/provider_packs/aws/*`
- Modify/Create: `custom_skills/arch-baseline/resources/provider_packs/azure/*`
- Modify/Create: `custom_skills/arch-baseline/resources/provider_packs/gcp/*`

**Step 1: Create pack.yml for each provider**

Required fields:
- provider, version, reviewed_at, recency_days
- pillars: canonical ids list (must match pillars.yml)
- defaults: review cadence/triggers, waiver defaults

**Step 2: Fill pillars.yml**

Include:
- canonical pillar names (and optional subpillars)
- review cadence defaults + triggers
- required evidence types per pillar
- waiver lifecycle defaults

**Step 3: Fill controls.yml**

Include normalized categories at minimum:
- identity_access
- logging_audit
- encryption_keys
- network
- observability
- backup_dr
- change_mgmt

Each entry must include:
- control_id (stable)
- provider_reference (provider-native concept)
- required_for (workloads/data classes)
- evidence_required
- normalization_target (registry + field path)

**Step 4: Fill constraints.yml**

Include:
- naming patterns
- environment taxonomy (dev/stage/prod)
- region/residency constraints hooks
- account/subscription/project layout rules

**Step 5: Fill validation_rules.yml**

Include:
- required baseline artifacts per provider (if any)
- WA pillar coverage checks (must match pack pillars)
- minimum required fields in registries after provider selection
- toolchain overlays required checks (kubernetes/terraform/cdk when enabled)
- crosslink requirements (baseline ↔ evidence ↔ registries ↔ WA plan)

**Step 6: Fill sources.yml**

Include:
- authoritative sources (MCP tools / doc categories)
- required recency policy
- topics → expected evidence items → normalization targets

### sources.yml v1 required authoritative sources (exact URLs)

These URLs are required inputs to preserve determinism and auditability. The provider pack validator MUST fail (exit 1) if any required `source_id` is missing.

**AWS required sources (minimum set)**
- Well-Architected pillars (6 pillars, includes Sustainability):
  - `https://docs.aws.amazon.com/wellarchitected/latest/framework/the-pillars-of-the-framework.html`
- Sustainability pillar deep-dive (explicit Sustainability pillar doc):
  - `https://docs.aws.amazon.com/wellarchitected/latest/sustainability-pillar/sustainability-pillar.html`
- GenAI / agents (for mandatory categories genai + ai_agents):
  - Amazon Bedrock documentation overview (includes Agents for Amazon Bedrock):
    - `https://aws.amazon.com/documentation-overview/bedrock/`
  - Amazon Bedrock Agents product overview (acceptable as v1 service reference locator):
    - `https://aws.amazon.com/bedrock/agents/`
- ML platform (for mandatory category machine_learning):
  - Amazon SageMaker documentation overview:
    - `https://aws.amazon.com/documentation-overview/sagemaker/`

**Azure required sources (minimum set)**
- Azure Well-Architected Framework overview (explicit 5 pillars):
  - `https://learn.microsoft.com/en-us/azure/well-architected/what-is-well-architected-framework`
- Azure Well-Architected pillars matrix:
  - `https://learn.microsoft.com/en-us/azure/well-architected/pillars`
- AI agents platform (for mandatory category ai_agents):
  - Foundry Agent Service overview:
    - `https://learn.microsoft.com/en-us/azure/ai-foundry/agents/overview`
- ML platform (for mandatory category machine_learning):
  - Azure Machine Learning documentation:
    - `https://learn.microsoft.com/en-us/azure/machine-learning/`
- Data analytics (for mandatory category data_analytics):
  - Azure Synapse Analytics overview:
    - `https://learn.microsoft.com/en-us/azure/synapse-analytics/overview-what-is`
- GenAI (for mandatory category genai):
  - Azure OpenAI Assistants function calling (explicit tool-calling reference locator):
    - `https://learn.microsoft.com/en-us/azure/ai-foundry/openai/how-to/assistant-functions`

**GCP required sources (minimum set)**
- Google Cloud Well-Architected Framework landing (pillar set + navigation):
  - `https://docs.cloud.google.com/architecture/framework`
- AI agents platform (for mandatory category ai_agents):
  - Vertex AI Agent Builder documentation:
    - `https://docs.cloud.google.com/agent-builder`
  - Vertex AI Agent Builder overview:
    - `https://docs.cloud.google.com/agent-builder/overview`
- ML + GenAI platform (for mandatory categories machine_learning + genai):
  - Vertex AI documentation:
    - `https://docs.cloud.google.com/vertex-ai/docs`
- Data analytics (for mandatory category data_analytics):
  - BigQuery documentation:
    - `https://docs.cloud.google.com/bigquery/docs`

**Acceptance test (enforceable)**
- For each provider pack, `sources.yml` includes all required `source_id`s and URLs above, and the validator asserts presence:
  - `python3 custom_skills/arch-baseline/scripts/validate_provider_pack.py --provider aws; echo "exit=$?"`
  - Expected: `exit=0` and output includes `✓ sources.yml required sources present`

**Negative test (fail-closed)**
- Remove one required source entry (example: delete the Azure pillars URL entry) and rerun:
  - `python3 custom_skills/arch-baseline/scripts/validate_provider_pack.py --provider azure; echo "exit=$?"`
  - Expected: `exit=1` and output includes:
    - `sources.yml missing required source_id: azure_waf_pillars`

Run: `python3 custom_skills/arch-baseline/scripts/validate_provider_pack.py --provider aws`
Expected: PASS.

**Step 7: Add tiered service catalogs + taxonomy (Provider Service Catalog, v1 core + optional full)**

Create a `services/` directory per provider pack. v1 requires a curated **core catalog** plus a mandatory taxonomy. A full inventory is optional and must be generated via an auditable pipeline.

Required files per provider pack:
- `custom_skills/arch-baseline/resources/provider_packs/<provider>/services/taxonomy.yml` (mandatory)
- `custom_skills/arch-baseline/resources/provider_packs/<provider>/services/services_core.yml` (mandatory)
- `custom_skills/arch-baseline/resources/provider_packs/<provider>/services/services_full.yml` (optional, generated)

Tier definitions:
- Tier 1 (mandatory): curated core catalog (80/20), sufficient to support common architecture decisions.
- Tier 2 (optional): full inventory, generated via MCP/web pipeline with audit/evidence/recency discipline.

MANDATORY taxonomy categories (must be present in taxonomy.yml)
Core platform:
- compute
- storage
- networking
- identity
- security
- observability
- governance_management
- devtools_cicd
- integration_messaging

Modern data+AI (also mandatory):
- data_analytics
  subcats: batch_etl, stream_processing, query_engine, data_warehouse, lakehouse, bi_visualization, data_catalog_governance
- machine_learning
  subcats: training, inference_hosting, feature_store, mlops_pipelines, model_registry, data_labeling, ml_monitoring
- genai
  subcats: foundation_models, prompt_orchestration, rag_tooling, vector_store, model_customization, safety_guardrails, evals_observability
- ai_agents
  subcats: agent_runtime, tool_connectors, function_calling, knowledge_connectors, workflow_orchestration, agent_observability, policy_governance

Required fields per services/services_core.yml entry
- service_id (stable provider-native identifier)
- display_name
- category (must match taxonomy)
- subcategory (optional; if present must match taxonomy subcats)
- short_description (1–2 sentences)
- key_capabilities (list; minItems 1)
- common_use_cases (list; minItems 1)
- pricing_model_hint (optional string)
- references (list of doc locators; may be empty in v1 only if `sources.yml` states where/how service catalog data is retrieved)

services_full.yml rules (enforced only if enabled by pack policy)
- must include `retrieved_at_utc`
- must include `source_locators` (or references per entry)
- must satisfy `recency_days` constraint
- must have tool-call audit + evidence coverage proving acquisition

**Enforceable acceptance criteria**
1) Each provider pack taxonomy.yml contains ALL mandatory categories above.
2) Each provider pack services_core.yml has >= 1 entry per mandatory category (core coverage), including the four data+AI categories:
   - data_analytics, machine_learning, genai, ai_agents
3) `python3 custom_skills/arch-baseline/scripts/validate_provider_pack.py --provider <provider>` returns exit code `0` and prints success lines including:
   - `✓ services taxonomy valid`
   - `✓ services_core schema valid`
   - `✓ services_core category coverage satisfied`

**Negative tests (fail-closed)**
1) Missing taxonomy => FAIL
- Move taxonomy out of the way:
  - `mv custom_skills/arch-baseline/resources/provider_packs/aws/services/taxonomy.yml /tmp/aws.taxonomy.bak`
- Run: `python3 custom_skills/arch-baseline/scripts/validate_provider_pack.py --provider aws; echo \"exit=$?\"`
- Expected: `exit=1` and output includes:
  - `Missing required file: custom_skills/arch-baseline/resources/provider_packs/aws/services/taxonomy.yml`
- Restore: `mv /tmp/aws.taxonomy.bak custom_skills/arch-baseline/resources/provider_packs/aws/services/taxonomy.yml`
2) Missing required category in core coverage => FAIL
- Remove all `ai_agents` category entries from services_core.yml and re-run:
  - `python3 custom_skills/arch-baseline/scripts/validate_provider_pack.py --provider aws; echo \"exit=$?\"`
  - Expected: `exit=1` and output includes:
    - `services_core missing required category: ai_agents`

**v2 expansion task (explicitly deferred)**
- Add a v2 milestone to expand services_full.yml toward a broader inventory using an auditable MCP/web pipeline (do not block v1).

## Task 4: Connect packs to baseline normalization (registries + adherence plan materialization)

**Files:**
- Create: `custom_skills/arch-baseline/scripts/load_provider_pack.py`
- Create: `custom_skills/arch-baseline/scripts/materialize_adherence_plan.py`
- Create: `custom_skills/arch-baseline/scripts/normalize_controls_to_registries.py`
- Modify: `custom_skills/arch-baseline/scripts/validate_baseline.py`
- Modify: `docs/baseline/baseline_manifest.json` (only if new artifacts are introduced)

**Step 1: load_provider_pack.py**

Load `pack.yml` + required YAMLs for the selected provider and return a normalized in-memory representation.

**Step 2: materialize_adherence_plan.py**

Given a selected provider:
- set frontmatter provider/framework fields
- write a provider-specific pillar mapping table derived from pack pillars + required doc families + evidence expectations

**Step 3: normalize_controls_to_registries.py**

Given pack controls.yml:
- upsert canonical IDs into:
  - `registries/security_controls_catalog.yml`
  - `registries/constraints_registry.yml`
  - `registries/slo_catalog.yml` (where applicable)

**Step 4: Provider-aware baseline validation**

Modify `validate_baseline.py` to:
- detect provider selection state (from adherence plan frontmatter)
- if provider is selected:
  - require provider pack presence and pack validation PASS
  - enforce provider-specific validation_rules.yml extensions
- if provider is unselected:
  - enforce template-mode adherence plan shape only

Run: `./tools/run_baseline_gate.sh`
Expected:
- PASS in template-mode (this repo)
- When switching provider to aws/azure/gcp: PASS only if pack is complete and registries meet minimum fields.

## Task 5: Add optional toolchain overlays (kubernetes/terraform/cdk)

**Files:**
- Create (optional per provider): `custom_skills/arch-baseline/resources/provider_packs/<provider>/overlays/*.yml`
- Modify: `custom_skills/arch-baseline/scripts/validate_provider_pack.py`
- Modify: `custom_skills/arch-baseline/scripts/validate_baseline.py`

**Step 1: Define overlay schemas**

Each overlay should define:
- baseline expectations (security/ops)
- evidence expectations
- validation hooks (e.g., required registry fields, required docs)

**Step 2: Activate overlays based on baseline_manifest toolchain flags**

If toolchain flag enabled (kubernetes/terraform/cdk):
- require overlay file exists for selected provider
- enforce overlay validation rules

## Task 6: Make the service catalog enforceable (schema + validator rules)

**Files:**
- Modify/Create: `custom_skills/arch-baseline/resources/schemas/provider_pack.schema.json`
- Create: `custom_skills/arch-baseline/resources/schemas/services.schema.json`
- Modify: `custom_skills/arch-baseline/scripts/validate_provider_pack.py`

**Step 1: Define services.schema.json**

Schema must enforce:
- taxonomy.yml:
  - top-level keys exist (e.g., `version`, `categories`)
  - `categories` includes all mandatory categories and their mandatory subcategories for data_analytics/machine_learning/genai/ai_agents
- services_core.yml:
  - top-level keys exist (e.g., `version`, `services`)
  - `services` is a non-empty array
  - each service object includes:
  - service_id (string, non-empty)
  - display_name (string, non-empty)
  - category (enum including required modern categories)
  - subcategory (optional; if present must be valid for the category)
  - short_description (string, min length, 1-2 sentences)
  - key_capabilities (array, minItems 1)
  - common_use_cases (array, minItems 1)
  - pricing_model_hint (string, optional)
  - references (array; may be empty only if pack sources.yml declares retrieval mechanism)

**Step 2: Extend validate_provider_pack.py (fail-closed)**

Validator must fail (exit 1) if:
- services/taxonomy.yml missing or invalid
- services/services_core.yml missing or invalid
- services_core.yml does not include at least one entry for each required modern category:
  - data_analytics, machine_learning, genai, ai_agents

**Acceptance test**
- `python3 custom_skills/arch-baseline/scripts/validate_provider_pack.py --provider aws`
  - Expected: exit code `0` and success output includes:
    - `✓ services taxonomy valid`
    - `✓ services_core schema valid`
    - `✓ services_core category coverage satisfied`

## Task 7: Ensure baseline gate links to provider pack validator

**Files:**
- Modify: `custom_skills/arch-baseline/scripts/validate_baseline.py`
- Modify: `tools/run_baseline_gate.sh`

**Step 1: Require validate_baseline.py to call validate_provider_pack.py when provider != unselected**

Enforcement rule:
- `provider == unselected` => template-mode allowed, do not require provider pack
- `provider in {aws,azure,gcp}` => must validate provider pack and fail closed on any pack error

**Step 2: Verify wrapper propagates failures**

Verification commands:
- `bash -x tools/run_baseline_gate.sh`
  - Expected: output shows an invocation path to baseline validation; and (when provider selected) a visible call to provider pack validation.

**Provider-selected negative test**
- Set `provider: aws` in `docs/baseline/WELL_ARCHITECTED_ADHERENCE_PLAN.md`
- Break pack deterministically (example: rename services_core.yml):
  - `mv custom_skills/arch-baseline/resources/provider_packs/aws/services/services_core.yml /tmp/aws.services_core.bak`
- Run: `./tools/run_baseline_gate.sh; echo \"exit=$?\"`
  - Expected: `exit=1` and output contains:
    - `Missing required file: custom_skills/arch-baseline/resources/provider_packs/aws/services/services_core.yml`
- Restore:
  - `mv /tmp/aws.services_core.bak custom_skills/arch-baseline/resources/provider_packs/aws/services/services_core.yml`

## Task 8: End-to-end acceptance tests

**Files:**
- Create: `custom_skills/arch-baseline/scripts/smoke_test_provider_packs.sh`

**Step 1: Template-mode baseline (provider unselected)**

Run:
`./tools/run_baseline_gate.sh`
Expected: PASS.

**Step 2: Provider selected (aws/azure/gcp)**

Temporarily set `provider:` in `docs/baseline/WELL_ARCHITECTED_ADHERENCE_PLAN.md` to one provider and run:
`./tools/run_baseline_gate.sh`
Expected: FAIL if pack incomplete; PASS when pack complete.

**Step 3: Reset back to template-mode**

Restore `provider: unselected` and confirm gate PASS.

## Task 9: Commit + push in logical chunks

**Files:**
- Modify/Create: as above

**Step 1: Commit validator and adherence plan template-mode**
`git add custom_skills/arch-baseline/scripts/validate_well_architected.py docs/baseline/WELL_ARCHITECTED_ADHERENCE_PLAN.md`
`git commit -m "feat: support provider-unselected adherence plan (template-mode)"`

**Step 2: Commit provider pack schema + validator**
`git add custom_skills/arch-baseline/resources/schemas/provider_pack.schema.json custom_skills/arch-baseline/resources/schemas/provider_services.schema.json custom_skills/arch-baseline/scripts/validate_provider_pack.py custom_skills/arch-baseline/resources/provider_packs/_templates/`
`git commit -m "feat: add provider pack schemas and validation"`

**Step 3: Commit provider packs v1**
`git add custom_skills/arch-baseline/resources/provider_packs/`
`git commit -m "feat: add v1 provider packs (aws/azure/gcp)"`

**Step 4: Commit pack-driven normalization + baseline provider-aware validation**
`git add custom_skills/arch-baseline/scripts/load_provider_pack.py custom_skills/arch-baseline/scripts/materialize_adherence_plan.py custom_skills/arch-baseline/scripts/normalize_controls_to_registries.py custom_skills/arch-baseline/scripts/validate_baseline.py`
`git commit -m "feat: pack-driven baseline normalization and validation"`

**Step 5: Commit baseline gate wrapper propagation**
`git add tools/run_baseline_gate.sh`
`git commit -m "chore: baseline gate propagates provider pack validation failures"`

**Step 5: Push**
`git push origin main`
