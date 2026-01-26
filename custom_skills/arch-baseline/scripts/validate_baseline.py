#!/usr/bin/env python3
"""
Baseline Gate Validation Wrapper
Validates that all required baseline output files exist and pass validation.
"""

import json
import sys
from pathlib import Path


def check_file_exists(file_path, description):
    """Check if a required file exists."""
    if Path(file_path).exists():
        print(f"✓ {description} exists: {file_path}")
        return True
    else:
        print(f"✗ {description} missing: {file_path}")
        return False


def run_well_architected_validation():
    """Run the Well-Architected adherence plan validator."""
    plan_file = "docs/baseline/WELL_ARCHITECTED_ADHERENCE_PLAN.md"

    if not Path(plan_file).exists():
        print(f"✗ Well-Architected Adherence Plan missing: {plan_file}")
        return False

    # Import and run the validator
    try:
        # Add the scripts directory to path to import the validator
        script_dir = Path(__file__).parent
        sys.path.insert(0, str(script_dir))

        from validate_well_architected import main as validate_main

        # Save original argv and temporarily replace it
        original_argv = sys.argv[:]
        sys.argv = ["validate_well_architected.py", plan_file]

        try:
            validate_main()
            print("✓ Well-Architected Adherence Plan validation passed")
            return True
        except SystemExit as e:
            if e.code == 0:
                print("✓ Well-Architected Adherence Plan validation passed")
                return True
            else:
                print("✗ Well-Architected Adherence Plan validation failed")
                return False
        finally:
            sys.argv = original_argv

    except ImportError as e:
        print(f"✗ Failed to import validator: {e}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error running validation: {e}")
        return False


def load_manifest(manifest_path: Path) -> dict | None:
    if not manifest_path.exists():
        print(f"✗ Baseline manifest missing: {manifest_path}")
        return None
    try:
        content = manifest_path.read_text(encoding="utf-8")
        return json.loads(content)
    except json.JSONDecodeError as exc:
        print(f"✗ Baseline manifest is invalid JSON: {exc}")
        return None
    except Exception as exc:  # pragma: no cover
        print(f"✗ Failed to read baseline manifest: {exc}")
        return None


def check_manifest_dependencies(manifest: dict) -> bool:
    ok = True
    baseline_index = manifest.get("paths", {}).get("baseline_docs_dir", "docs/baseline")
    # Explicit files to check
    required_files = [
        ("docs/baseline/SYSTEM_CHARTER.md", "System Charter"),
        ("docs/baseline/C4_Context.md", "C4 Context Diagram"),
        ("docs/baseline/C4_Container.md", "C4 Container Diagram"),
        ("docs/baseline/CLOUD_PROVIDER_DECISION_ADR.md", "Cloud Provider Decision ADR"),
        ("docs/baseline/BASELINE_INDEX.md", "Baseline Index"),
        ("docs/baseline/BASELINE_HANDOFF.md", "Baseline Handoff"),
    ]

    paths_section = manifest.get("paths", {})
    audit_files = [
        (
            paths_section.get(
                "evidence_log_jsonl", "docs/audit/evidence/evidence_log.jsonl"
            ),
            "Evidence log (jsonl)",
        ),
        (
            paths_section.get(
                "tool_call_audit_jsonl", "docs/audit/tool_calls/tool_call_audit.jsonl"
            ),
            "Tool-call audit log",
        ),
    ]

    registries = manifest.get("registries", [])

    print("\n1. Checking required baseline files...")
    for file_path, description in required_files:
        if not check_file_exists(file_path, description):
            ok = False

    print("\n2. Checking audit artifacts...")
    for file_path, description in audit_files:
        if not file_path:
            continue
        if not check_file_exists(file_path, description):
            ok = False

    print("\n3. Checking registries...")
    for registry in registries:
        path = registry.get("path")
        if not path:
            continue
        if not check_file_exists(path, f"Registry {registry.get('id', '')}"):
            ok = False

    return ok


def main():
    """Main baseline gate validation."""
    print("=== BASELINE GATE VALIDATION ===")

    manifest_path = Path("docs/baseline/baseline_manifest.json")
    manifest = load_manifest(manifest_path)
    all_passed = True

    if manifest is None:
        all_passed = False
    else:
        if not check_manifest_dependencies(manifest):
            all_passed = False

    print("\n4. Validating Well-Architected Adherence Plan...")
    if not run_well_architected_validation():
        all_passed = False

    print("\n=== BASELINE GATE RESULT ===")
    if all_passed:
        print("✓ BASELINE GATE PASSED - All requirements satisfied")
        print("Ready to proceed with arch-docs and impl-strategy")
        sys.exit(0)
    else:
        print("✗ BASELINE GATE FAILED - Fix issues before proceeding")
        print("arch-docs and impl-strategy will be blocked")
        sys.exit(1)


if __name__ == "__main__":
    main()
