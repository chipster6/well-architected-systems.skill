#!/usr/bin/env python3
"""
Provider pack validator (fail-closed).

This validates that a selected provider pack exists, is structurally complete,
and satisfies enforceable policy requirements (including service taxonomy + core
coverage and required authoritative sources).

No external dependencies (PyYAML) are used; packs must conform to a strict YAML
subset consumed by _yaml_subset.py.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from _yaml_subset import YamlSubsetError, load_yaml


PACK_ROOT_DEFAULT = Path("custom_skills/arch-baseline/resources/provider_packs")
SUPPORTED_PROVIDERS = {"aws", "azure", "gcp"}


REQUIRED_FILES = [
    "pack.yml",
    "pillars.yml",
    "controls.yml",
    "constraints.yml",
    "validation_rules.yml",
    "sources.yml",
    "services/taxonomy.yml",
    "services/services_core.yml",
]


MANDATORY_TAXONOMY = {
    "compute": [],
    "storage": [],
    "networking": [],
    "identity": [],
    "security": [],
    "observability": [],
    "governance_management": [],
    "devtools_cicd": [],
    "integration_messaging": [],
    "data_analytics": [
        "batch_etl",
        "stream_processing",
        "query_engine",
        "data_warehouse",
        "lakehouse",
        "bi_visualization",
        "data_catalog_governance",
    ],
    "machine_learning": [
        "training",
        "inference_hosting",
        "feature_store",
        "mlops_pipelines",
        "model_registry",
        "data_labeling",
        "ml_monitoring",
    ],
    "genai": [
        "foundation_models",
        "prompt_orchestration",
        "rag_tooling",
        "vector_store",
        "model_customization",
        "safety_guardrails",
        "evals_observability",
    ],
    "ai_agents": [
        "agent_runtime",
        "tool_connectors",
        "function_calling",
        "knowledge_connectors",
        "workflow_orchestration",
        "agent_observability",
        "policy_governance",
    ],
}


# Enforceable minimum authoritative sources required in sources.yml.
# The plan documents exact URLs; the validator enforces presence by source_id.
REQUIRED_SOURCE_IDS = {
    "aws": {
        "aws_wa_pillars",
        "aws_wa_sustainability_pillar",
        "aws_bedrock_docs_overview",
        "aws_bedrock_agents_overview",
        "aws_sagemaker_docs_overview",
    },
    "azure": {
        "azure_waf_overview",
        "azure_waf_pillars",
        "azure_ai_foundry_agents_overview",
        "azure_ml_docs",
        "azure_synapse_overview",
        "azure_openai_assistant_functions",
    },
    "gcp": {
        "gcp_arch_framework",
        "gcp_agent_builder_docs",
        "gcp_agent_builder_overview",
        "gcp_vertex_ai_docs",
        "gcp_bigquery_docs",
    },
}


def _err(msg: str) -> None:
    print(f"ERROR: {msg}")


def _ok(msg: str) -> None:
    print(f"✓ {msg}")


def _require(condition: bool, msg: str) -> bool:
    if not condition:
        _err(msg)
        return False
    return True


def _load_yaml_required(path: Path) -> tuple[bool, object | None]:
    try:
        return True, load_yaml(str(path))
    except FileNotFoundError:
        _err(f"Missing required file: {path}")
        return False, None
    except YamlSubsetError as exc:
        _err(str(exc))
        return False, None
    except Exception as exc:  # pragma: no cover
        _err(f"Failed to load YAML: {path}: {exc}")
        return False, None


def validate_required_files(pack_dir: Path) -> bool:
    ok = True
    for rel in REQUIRED_FILES:
        p = pack_dir / rel
        if not p.exists():
            _err(f"Missing required file: {p}")
            ok = False
    return ok


def validate_pack_metadata(provider: str, pack_yml: dict) -> bool:
    ok = True
    for k in ("provider", "version", "reviewed_at", "recency_days"):
        ok &= _require(k in pack_yml, f"pack.yml: missing required key: {k}")
    if "provider" in pack_yml:
        ok &= _require(pack_yml["provider"] == provider, f"pack.yml: provider mismatch: {pack_yml['provider']} != {provider}")
    if "pillar_ids" in pack_yml:
        pillar_ids = pack_yml.get("pillar_ids")
        ok &= _require(isinstance(pillar_ids, list) and pillar_ids, "pack.yml: pillar_ids must be a non-empty list")
    return ok


def validate_sources(provider: str, sources_yml: dict) -> bool:
    if not isinstance(sources_yml, dict):
        _err("sources.yml must be a mapping")
        return False
    sources = sources_yml.get("sources")
    if not isinstance(sources, list):
        _err("sources.yml: 'sources' must be a list")
        return False

    found_ids: set[str] = set()
    for item in sources:
        if isinstance(item, dict) and "source_id" in item:
            found_ids.add(str(item["source_id"]))

    required = REQUIRED_SOURCE_IDS.get(provider, set())
    missing = sorted(required - found_ids)
    if missing:
        for mid in missing:
            _err(f"sources.yml missing required source_id: {mid}")
        return False
    _ok("sources.yml required sources present")
    return True


def validate_taxonomy(taxonomy_yml: dict) -> bool:
    ok = True
    if not isinstance(taxonomy_yml, dict):
        _err("taxonomy.yml must be a mapping")
        return False
    categories = taxonomy_yml.get("categories")
    ok &= _require(isinstance(categories, dict), "taxonomy.yml: categories must be a mapping")
    if not isinstance(categories, dict):
        return False

    for cat, subcats in MANDATORY_TAXONOMY.items():
        ok &= _require(cat in categories, f"taxonomy.yml missing mandatory category: {cat}")
        if cat not in categories:
            continue
        declared_subcats = categories.get(cat, {}).get("subcategories", [])
        if subcats:
            ok &= _require(
                isinstance(declared_subcats, list),
                f"taxonomy.yml: categories.{cat}.subcategories must be a list",
            )
            if isinstance(declared_subcats, list):
                for sc in subcats:
                    ok &= _require(
                        sc in declared_subcats,
                        f"taxonomy.yml: missing subcategory '{sc}' under '{cat}'",
                    )

    if ok:
        _ok("services taxonomy valid")
    return ok


def validate_services_core(provider: str, core_yml: dict) -> bool:
    ok = True
    if not isinstance(core_yml, dict):
        _err("services_core.yml must be a mapping")
        return False

    services = core_yml.get("services")
    ok &= _require(isinstance(services, list) and services, "services_core.yml: services must be a non-empty list")
    if not isinstance(services, list):
        return False

    required_fields = [
        "service_id",
        "display_name",
        "category",
        "short_description",
        "key_capabilities",
        "common_use_cases",
        "references",
    ]

    seen_categories: set[str] = set()
    for idx, svc in enumerate(services):
        if not isinstance(svc, dict):
            _err(f"services_core.yml: services[{idx}] must be a mapping")
            ok = False
            continue
        for rf in required_fields:
            if rf not in svc:
                _err(f"services_core.yml: services[{idx}] missing required field: {rf}")
                ok = False
        cat = svc.get("category")
        if isinstance(cat, str):
            seen_categories.add(cat)
        # list fields
        for lf in ("key_capabilities", "common_use_cases", "references"):
            if lf in svc and not (isinstance(svc[lf], list) and len(svc[lf]) >= 0):
                _err(f"services_core.yml: services[{idx}].{lf} must be a list")
                ok = False
        if "key_capabilities" in svc and isinstance(svc["key_capabilities"], list) and len(svc["key_capabilities"]) < 1:
            _err(f"services_core.yml: services[{idx}].key_capabilities must have at least 1 item")
            ok = False
        if "common_use_cases" in svc and isinstance(svc["common_use_cases"], list) and len(svc["common_use_cases"]) < 1:
            _err(f"services_core.yml: services[{idx}].common_use_cases must have at least 1 item")
            ok = False

    # Coverage: require >=1 entry for each mandatory category
    for cat in MANDATORY_TAXONOMY.keys():
        if cat not in seen_categories:
            _err(f"services_core missing required category: {cat}")
            ok = False

    if ok:
        _ok("services_core schema valid")
        _ok("services_core category coverage satisfied")
    return ok


def validate_provider_pack(provider: str, pack_root: Path) -> int:
    if provider not in SUPPORTED_PROVIDERS:
        _err(f"Unknown provider: {provider}")
        return 2

    pack_dir = pack_root / provider
    if not pack_dir.exists():
        _err(f"Missing provider pack directory: {pack_dir}")
        return 1

    ok = validate_required_files(pack_dir)
    if not ok:
        return 1

    ok_pack, pack_yml = _load_yaml_required(pack_dir / "pack.yml")
    ok_pillars, _pillars_yml = _load_yaml_required(pack_dir / "pillars.yml")
    ok_controls, _controls_yml = _load_yaml_required(pack_dir / "controls.yml")
    ok_constraints, _constraints_yml = _load_yaml_required(pack_dir / "constraints.yml")
    ok_rules, _rules_yml = _load_yaml_required(pack_dir / "validation_rules.yml")
    ok_sources, sources_yml = _load_yaml_required(pack_dir / "sources.yml")
    ok_tax, taxonomy_yml = _load_yaml_required(pack_dir / "services/taxonomy.yml")
    ok_core, core_yml = _load_yaml_required(pack_dir / "services/services_core.yml")

    ok = ok and ok_pack and ok_pillars and ok_controls and ok_constraints and ok_rules and ok_sources and ok_tax and ok_core
    if not ok:
        return 1

    assert isinstance(pack_yml, dict)
    assert isinstance(sources_yml, dict)
    assert isinstance(taxonomy_yml, dict)
    assert isinstance(core_yml, dict)

    ok &= validate_pack_metadata(provider, pack_yml)
    ok &= validate_sources(provider, sources_yml)
    ok &= validate_taxonomy(taxonomy_yml)
    ok &= validate_services_core(provider, core_yml)

    return 0 if ok else 1


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--provider", required=True)
    parser.add_argument("--pack-root", default=str(PACK_ROOT_DEFAULT))
    args = parser.parse_args()

    code = validate_provider_pack(args.provider, Path(args.pack_root))
    sys.exit(code)


if __name__ == "__main__":
    main()
