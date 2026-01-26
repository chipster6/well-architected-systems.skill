#!/usr/bin/env python3
"""
Baseline Gate Validation Wrapper
Validates that all required baseline output files exist and pass validation.
"""

import sys
import os
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


def main():
    """Main baseline gate validation."""
    print("=== BASELINE GATE VALIDATION ===")

    # Required baseline files
    required_files = [
        ("docs/baseline/SYSTEM_CHARTER.md", "System Charter"),
        ("docs/baseline/C4_Context.md", "C4 Context Diagram"),
        ("docs/baseline/C4_Container.md", "C4 Container Diagram"),
        ("docs/baseline/CLOUD_PROVIDER_DECISION_ADR.md", "Cloud Provider Decision ADR"),
    ]

    all_passed = True

    # Check required files exist
    print("\n1. Checking required baseline files...")
    for file_path, description in required_files:
        if not check_file_exists(file_path, description):
            all_passed = False

    # Validate Well-Architected Adherence Plan
    print("\n2. Validating Well-Architected Adherence Plan...")
    if not run_well_architected_validation():
        all_passed = False

    # Summary
    print(f"\n=== BASELINE GATE RESULT ===")
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
