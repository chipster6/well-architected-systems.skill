#!/usr/bin/env python3
"""
Architecture Documentation Validation
Validates architecture documentation with mandatory baseline gate dependency.
"""

import shutil
import subprocess
import sys
from pathlib import Path


def repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def python_interpreter() -> str:
    if sys.executable:
        return sys.executable
    for candidate in ("python3", "python"):
        cmd = shutil.which(candidate)
        if cmd:
            return cmd
    raise RuntimeError("No python interpreter available")


def run_baseline_gate() -> bool:
    print("=== CHECKING BASELINE GATE ===")
    validator = repo_root() / "custom_skills/arch-baseline/scripts/validate_baseline.py"
    if not validator.exists():
        print(f"✗ Baseline validator missing: {validator}")
        return False

    try:
        result = subprocess.run(
            [python_interpreter(), str(validator)],
            capture_output=True,
            text=True,
            cwd=repo_root(),
        )
    except Exception as exc:  # pragma: no cover
        print(f"✗ Error running baseline gate: {exc}")
        return False

    if result.returncode == 0:
        print("✓ BASELINE GATE PASSED")
        return True

    print("✗ BASELINE GATE FAILED")
    if result.stdout:
        print(result.stdout.strip())
    if result.stderr:
        print("STDERR:", result.stderr.strip())
    return False


def check_required_files() -> list[str]:
    errors: list[str] = []
    root = repo_root()
    required_files = [
        (
            root / "custom_skills/arch-docs/resources/policy/required_sections.yml",
            "Required sections policy",
        ),
        (
            root / "custom_skills/arch-docs/resources/policy/crosslink_rules.yml",
            "Crosslink rules policy",
        ),
        (
            root / "custom_skills/arch-docs/resources/policy/placeholder_rules.yml",
            "Placeholder rules policy",
        ),
    ]

    for file_path, description in required_files:
        if not file_path.exists():
            errors.append(f"Missing {description}: {file_path}")
        elif file_path.stat().st_size == 0:
            errors.append(f"{description} is empty: {file_path}")

    arch_dir = root / "docs/architecture"
    if not arch_dir.exists() or not arch_dir.is_dir():
        errors.append(f"Architecture documentation directory missing: {arch_dir}")

    return errors


def main():
    print("=== ARCH-DOCS VALIDATION ===")

    if not run_baseline_gate():
        print("Architecture documentation gate blocked by baseline failures")
        sys.exit(1)

    print("\n=== VALIDATING ARCHITECTURE DOC REQUIREMENTS ===")
    errors = check_required_files()

    if errors:
        print("Validation failed:")
        for idx, err in enumerate(errors, 1):
            print(f"  {idx}. {err}")
        sys.exit(1)

    print("✓ Architecture documentation prerequisites satisfied")
    sys.exit(0)


if __name__ == "__main__":
    main()
