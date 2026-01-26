#!/usr/bin/env bash
#
# Architecture Documentation Gate Wrapper Script
# Invokes the arch-docs validator with deterministic behavior.
#

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
VALIDATOR="custom_skills/arch-docs/scripts/validate_docs.py"

cd "$REPO_ROOT"

if [[ ! -f "$VALIDATOR" ]]; then
	echo "ERROR: Architecture docs validator not found at $VALIDATOR" >&2
	exit 1
fi

if command -v python3 >/dev/null 2>&1; then
	PYTHON_CMD="python3"
elif command -v python >/dev/null 2>&1; then
	PYTHON_CMD="python"
else
	echo "ERROR: python or python3 interpreter not found in PATH" >&2
	exit 1
fi

"$PYTHON_CMD" "$VALIDATOR"

echo "Architecture documentation gate completed successfully"
