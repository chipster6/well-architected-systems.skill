#!/usr/bin/env python3
import json
import os
import sys

from jsonschema import Draft202012Validator

ROOT = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(ROOT, os.pardir))
SCHEMA_DIR = os.path.join(ROOT, "schemas")
EXAMPLES_DIR = os.path.join(ROOT, "assets", "examples")

SCHEMAS = {
    "mcp_evidence_log.schema.json": os.path.join(
        SCHEMA_DIR, "mcp_evidence_log.schema.json"
    ),
    "phase_completion_report.schema.json": os.path.join(
        SCHEMA_DIR, "phase_completion_report.schema.json"
    ),
    "well_architected_pillar_matrix.schema.json": os.path.join(
        SCHEMA_DIR, "well_architected_pillar_matrix.schema.json"
    ),
    "claim_index.schema.json": os.path.join(SCHEMA_DIR, "claim_index.schema.json"),
}

EXAMPLE_MAP = {
    "mcp_evidence_log.schema.json": os.path.join(
        EXAMPLES_DIR, "MCP_EVIDENCE_LOG.example.json"
    ),
    "phase_completion_report.schema.json": os.path.join(
        EXAMPLES_DIR, "PHASE_COMPLETION_REPORT_P0.example.json"
    ),
    "well_architected_pillar_matrix.schema.json": os.path.join(
        EXAMPLES_DIR, "WELL_ARCHITECTED_PILLAR_MATRIX.example.json"
    ),
    "claim_index.schema.json": os.path.join(EXAMPLES_DIR, "CLAIM_INDEX.example.json"),
}


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def validate_schema(name, schema_path):
    try:
        schema = load_json(schema_path)
        Draft202012Validator.check_schema(schema)
    except Exception as exc:  # noqa: BLE001
        print(f"schema {name} invalid: {exc}")
        return False
    return True


def validate_example(schema_name, schema_path, example_path):
    schema = load_json(schema_path)
    data = load_json(example_path)
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(data), key=lambda e: e.path)
    if errors:
        print(
            f"example {os.path.basename(example_path)} failed validation against {schema_name}:"
        )
        for err in errors:
            print(f" - {list(err.path)}: {err.message}")
        return False
    return True


def main():
    ok = True
    for name, path in SCHEMAS.items():
        if not validate_schema(name, path):
            ok = False
    for schema_name, example_path in EXAMPLE_MAP.items():
        if not os.path.exists(example_path):
            print(f"example missing for {schema_name}: {example_path}")
            ok = False
            continue
        schema_path = SCHEMAS[schema_name]
        if not validate_example(schema_name, schema_path, example_path):
            ok = False
    if ok:
        print("validate_skill_artifacts: PASS")
        sys.exit(0)
    sys.exit(1)


if __name__ == "__main__":
    main()
