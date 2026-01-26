#!/usr/bin/env python3
"""
Implementation Strategy Task Graph Validation
Validates implementation strategy and task graphs with mandatory baseline gate dependency.
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


def check_required_assets() -> list[str]:
    errors: list[str] = []
    root = repo_root()
    policy_file = (
        root / "custom_skills/impl-strategy/resources/policy/gate_definitions.yml"
    )
    if not policy_file.exists():
        errors.append(f"Missing gate definitions policy: {policy_file}")
    elif policy_file.stat().st_size == 0:
        errors.append(f"Gate definitions policy is empty: {policy_file}")

    impl_dir = root / "docs/implementation"
    if not impl_dir.exists() or not impl_dir.is_dir():
        errors.append(f"Implementation documentation directory missing: {impl_dir}")

    return errors


def main():
    print("=== IMPLEMENTATION STRATEGY VALIDATION ===")

    if not run_baseline_gate():
        print("Implementation strategy gate blocked by baseline failures")
        sys.exit(1)

    print("\n=== VALIDATING IMPLEMENTATION STRATEGY REQUIREMENTS ===")
    errors = check_required_assets()

    if errors:
        print("Validation failed:")
        for idx, err in enumerate(errors, 1):
            print(f"  {idx}. {err}")
        sys.exit(1)

    print("✓ Implementation strategy prerequisites satisfied")
    sys.exit(0)


if __name__ == "__main__":
    main()
