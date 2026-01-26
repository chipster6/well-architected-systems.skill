#!/usr/bin/env python3
"""
Architecture Documentation Validation
Validates architecture documentation with mandatory baseline gate dependency.
"""

import sys
import os
import subprocess
from pathlib import Path


def run_baseline_gate():
    """Run the baseline gate check."""
    print("=== CHECKING BASELINE GATE ===")

    # Change to repo root
    repo_root = Path(__file__).parent.parent.parent
    os.chdir(repo_root)

    try:
        # Run baseline gate script
        result = subprocess.run(
            ["python", "custom_skills/arch-baseline/scripts/validate_baseline.py"],
            capture_output=True,
            text=True,
        )

        if result.returncode == 0:
            print("✓ BASELINE GATE PASSED")
            return True
        else:
            print("✗ BASELINE GATE FAILED")
            print(result.stdout)
            if result.stderr:
                print("STDERR:", result.stderr)
            return False

    except FileNotFoundError:
        print("✗ Could not find baseline validation script")
        return False
    except Exception as e:
        print(f"✗ Error running baseline gate: {e}")
        return False


def main():
    """Main validation with baseline dependency."""
    print("=== ARCH-DOCS VALIDATION ===")

    # Step 1: Baseline gate check
    if not run_baseline_gate():
        print("\nBASELINE GATE FAILED")
        print("Architecture documentation cannot proceed until baseline passes.")
        sys.exit(1)

    print("\n=== PROCEEDING WITH DOCUMENTATION VALIDATION ===")

    # TODO: Implement full documentation validation
    # For now, just check that docs/architecture directory exists
    arch_dir = Path("docs/architecture")
    if arch_dir.exists():
        print(f"✓ Architecture directory exists: {arch_dir}")
        print("✓ Documentation validation placeholder passed")
        sys.exit(0)
    else:
        print(f"! Architecture directory not found: {arch_dir}")
        print("! This is expected for new repositories")
        print("✓ Documentation validation placeholder passed")
        sys.exit(0)


if __name__ == "__main__":
    main()
