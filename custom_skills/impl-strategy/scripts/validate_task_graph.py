#!/usr/bin/env python3
"""
Implementation Strategy Task Graph Validation
Validates implementation strategy and task graphs with mandatory baseline gate dependency.
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
    print("=== IMPLEMENTATION STRATEGY VALIDATION ===")

    # Step 1: Baseline gate check
    if not run_baseline_gate():
        print("\nBASELINE GATE FAILED")
        print("Implementation strategy cannot proceed until baseline passes.")
        sys.exit(1)

    print("\n=== PROCEEDING WITH TASK GRAPH VALIDATION ===")

    # TODO: Implement full task graph validation
    # For now, just check that docs/implementation directory exists
    impl_dir = Path("docs/implementation")
    if impl_dir.exists():
        print(f"✓ Implementation directory exists: {impl_dir}")
        print("✓ Task graph validation placeholder passed")
        sys.exit(0)
    else:
        print(f"! Implementation directory not found: {impl_dir}")
        print("! This is expected for new repositories")
        print("✓ Task graph validation placeholder passed")
        sys.exit(0)


if __name__ == "__main__":
    main()
