#!/usr/bin/env python3
"""
Scaffold Architecture Docs
Generates architecture documentation from templates and baseline manifest.
"""

import argparse
import json
import os
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path


def run_baseline_gate():
    """Run baseline gate to ensure we can proceed."""
    repo_root = Path(__file__).parent.parent.parent.parent
    gate_script = repo_root / "tools" / "run_baseline_gate.sh"

    if not gate_script.exists():
        print("✗ Baseline gate script missing")
        return False

    import subprocess
    result = subprocess.run([str(gate_script)], capture_output=True, text=True)
    if result.returncode != 0:
        print("✗ Baseline gate failed")
        print(result.stdout)
        return False
    return True


def scaffold_docs(target_dir: Path):
    """Scaffold architecture documentation."""
    print(f"Scaffolding architecture docs in: {target_dir}")

    if not run_baseline_gate():
        sys.exit(1)

    repo_root = Path(__file__).parent.parent.parent.parent
    templates_base = repo_root / "custom_skills" / "arch-docs" / "resources" / "templates"
    arch_docs_dir = target_dir / "docs" / "architecture"

    arch_docs_dir.mkdir(parents=True, exist_ok=True)
    print(f"✓ Ensured directory: {arch_docs_dir}")

    # Map templates to target files
    template_map = {
        "architecture/ARC_OVERVIEW.md": "ARC_OVERVIEW.md",
        "well-architected/WELL_ARCHITECTED_PILLAR_MATRIX.md": "WELL_ARCHITECTED_PILLAR_MATRIX.md",
        "security/THREAT_MODEL.md": "THREAT_MODEL.md",
        "ops/RUNBOOK.md": "OPERATIONS_MODEL.md",
    }

    for rel_path, dest_name in template_map.items():
        template_path = templates_base / rel_path
        dest_path = arch_docs_dir / dest_name

        if template_path.exists():
            if not dest_path.exists():
                shutil.copy2(template_path, dest_path)
                print(f"✓ Created: {dest_path}")
            else:
                print(f"! Skipping existing file: {dest_path}")
        else:
            print(f"! Template not found: {template_path}")

    # Initialize Index
    index_path = arch_docs_dir / "ARCHITECTURE_INDEX.md"
    if not index_path.exists():
        index_content = "# Architecture Documentation Index\n\n"
        index_content += "## Core Documents\n"
        for dest_name in template_map.values():
            index_content += f"- [{dest_name.replace('.md', '')}]({dest_name})\n"

        index_path.write_text(index_content)
        print(f"✓ Created index: {index_path}")

    print("\nArchitecture scaffolding complete.")


def main():
    parser = argparse.ArgumentParser(description="Scaffold architecture documentation.")
    parser.add_argument("--target", type=str, default=".", help="Target directory (default: current)")
    args = parser.parse_args()

    scaffold_docs(Path(args.target))


if __name__ == "__main__":
    main()
