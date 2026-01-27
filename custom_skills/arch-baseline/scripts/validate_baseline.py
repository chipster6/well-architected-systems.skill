#!/usr/bin/env python3
"""
Baseline Gate Validation Wrapper
Validates that all required baseline output files exist and pass validation.
"""

import argparse
import json
import sys
from pathlib import Path


def check_path_exists(path: Path, description: str, expected_type: str | None = None):
    """Check if a required file/directory exists."""
    if not path.exists():
        print(f"✗ {description} missing: {path}")
        return False
    if expected_type == "directory" and not path.is_dir():
        print(f"✗ {description} is not a directory: {path}")
        return False
    if expected_type != "directory" and path.is_dir():
        print(f"✗ {description} is a directory, expected file: {path}")
        return False
    print(f"✓ {description} exists: {path}")
    return True


def is_effectively_empty_file(path: Path) -> bool:
    """Treat whitespace/comment-only or YAML empty values as empty."""
    try:
        content = path.read_text(encoding="utf-8")
    except Exception:
        return True

    meaningful: list[str] = []
    for line in content.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or stripped == "---":
            continue
        meaningful.append(stripped)

    if not meaningful:
        return True
    if len(meaningful) == 1 and meaningful[0] in ("[]", "{}", "null", "~"):
        return True
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


def get_selected_provider_from_adherence_plan() -> str | None:
    """Return provider from adherence plan YAML frontmatter."""
    plan_file = "docs/baseline/WELL_ARCHITECTED_ADHERENCE_PLAN.md"
    try:
        script_dir = Path(__file__).parent
        sys.path.insert(0, str(script_dir))
        from validate_well_architected import load_yaml_frontmatter

        frontmatter, _markdown = load_yaml_frontmatter(plan_file)
        if not frontmatter:
            return None
        provider = frontmatter.get("provider")
        return provider if isinstance(provider, str) else None
    except Exception:
        return None


def run_provider_pack_validation(provider: str) -> bool:
    """Run provider pack validation for the selected provider (fail-closed)."""
    try:
        script_dir = Path(__file__).parent
        sys.path.insert(0, str(script_dir))

        from validate_provider_pack import validate_provider_pack

        code = validate_provider_pack(provider, Path("custom_skills/arch-baseline/resources/provider_packs"))
        if code == 0:
            print("✓ Provider pack validation passed")
            return True
        print("✗ Provider pack validation failed")
        return False
    except ImportError as e:
        print(f"✗ Failed to import provider pack validator: {e}")
        return False
    except Exception as e:  # pragma: no cover
        print(f"✗ Unexpected error running provider pack validation: {e}")
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


def check_manifest_dependencies(manifest: dict, fail_empty_registries: bool) -> bool:
    ok = True
    artifacts = manifest.get("artifacts", [])
    registries = manifest.get("registries", [])

    print("\n1. Checking manifest artifacts (mandatory)...")
    for artifact in artifacts:
        if not artifact.get("mandatory"):
            continue
        raw_path = artifact.get("path", "")
        if not raw_path:
            print(f"✗ Artifact {artifact.get('id', '')} missing path in manifest")
            ok = False
            continue
        path = Path(raw_path)
        expected_type = "directory" if artifact.get("type") == "directory" else None
        if not check_path_exists(path, f"Artifact {artifact.get('id', '')}", expected_type):
            ok = False

    print("\n2. Checking registries (mandatory)...")
    for registry in registries:
        if not registry.get("mandatory"):
            continue
        raw_path = registry.get("path", "")
        if not raw_path:
            print(f"✗ Registry {registry.get('id', '')} missing path in manifest")
            ok = False
            continue
        path = Path(raw_path)
        if not check_path_exists(path, f"Registry {registry.get('id', '')}"):
            ok = False

    if fail_empty_registries:
        print("\n3. Checking registries (non-empty, mandatory)...")
        for registry in registries:
            if not registry.get("mandatory"):
                continue
            raw_path = registry.get("path", "")
            if not raw_path:
                continue
            path = Path(raw_path)
            if path.exists() and is_effectively_empty_file(path):
                print(f"✗ Registry {registry.get('id', '')} is empty: {path}")
                ok = False
            elif path.exists():
                print(f"✓ Registry {registry.get('id', '')} is non-empty: {path}")

    return ok


def main():
    """Main baseline gate validation."""
    print("=== BASELINE GATE VALIDATION ===")

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--allow-empty-registries",
        action="store_true",
        help="Do not fail the gate when mandatory registries are empty",
    )
    args = parser.parse_args()

    manifest_path = Path("docs/baseline/baseline_manifest.json")
    manifest = load_manifest(manifest_path)
    all_passed = True

    if manifest is None:
        all_passed = False
    else:
        if not check_manifest_dependencies(manifest, not args.allow_empty_registries):
            all_passed = False

    print("\n4. Validating Well-Architected Adherence Plan...")
    if not run_well_architected_validation():
        all_passed = False

    provider = get_selected_provider_from_adherence_plan()
    if provider and provider != "unselected":
        print("\n5. Validating provider pack (provider-selected mode)...")
        if not run_provider_pack_validation(provider):
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
