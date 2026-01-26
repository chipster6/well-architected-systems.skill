#!/bin/bash
#
# Baseline Gate Wrapper Script
# Runs the baseline validation and returns appropriate exit codes
#
# Usage: ./tools/run_baseline_gate.sh
#

set -e # Exit on any error

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "Running baseline gate from repository root: $REPO_ROOT"
cd "$REPO_ROOT"

# Run the Python baseline validator
python custom_skills/arch-baseline/scripts/validate_baseline.py

# If we get here, validation passed
echo "Baseline gate check completed successfully"
