#!/usr/bin/env bash
#
# Implementation Strategy Gate Wrapper Script
# Invokes the impl-strategy validator deterministically.
#

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
VALIDATOR="custom_skills/impl-strategy/scripts/validate_task_graph.py"

cd "$REPO_ROOT"

if [[ ! -f "$VALIDATOR" ]]; then
	echo "ERROR: Implementation strategy validator not found at $VALIDATOR" >&2
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

echo "Implementation strategy gate completed successfully"
