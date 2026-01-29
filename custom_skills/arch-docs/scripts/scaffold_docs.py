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
import re
from datetime import datetime, timezone
from pathlib import Path

def parse_simple_yaml(text):
    """
    Simple YAML parser for the specific structure used in catalogs.
    """
    result = {}
    lines = text.splitlines()
    current_key = None
    current_list = None
    current_item = None

    for line in lines:
        line = line.rstrip()
        if not line or line.strip().startswith('#'):
            continue

        indent = len(line) - len(line.lstrip())
        stripped = line.strip()

        if stripped.startswith('-'):
            if current_list is not None:
                if current_item is not None:
                    current_list.append(current_item)
                current_item = {}
                rest = stripped[1:].strip()
                if ':' in rest:
                    k, v = rest.split(':', 1)
                    current_item[k.strip()] = v.strip().strip('"').strip("'")
            continue

        if ':' in stripped:
            k, v = stripped.split(':', 1)
            k = k.strip()
            v = v.strip().strip('"').strip("'")

            if not v:
                if current_item is not None and indent > 0:
                    current_item[k] = [] # Nested list (not fully supported)
                else:
                    current_key = k
                    current_list = []
                    result[current_key] = current_list
                    current_item = None
            else:
                if current_item is not None:
                    current_item[k] = v
                else:
                    result[k] = v

    if current_list is not None and current_item is not None:
        current_list.append(current_item)

    return result

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
    services_dir = arch_docs_dir / "services"

    arch_docs_dir.mkdir(parents=True, exist_ok=True)
    services_dir.mkdir(parents=True, exist_ok=True)
    print(f"✓ Ensured directories: {arch_docs_dir}, {services_dir}")

    # Map templates to target files
    template_map = {
        "architecture/ARC_OVERVIEW.md": "ARC_OVERVIEW.md",
        "well-architected/WELL_ARCHITECTED_PILLAR_MATRIX.md": "WELL_ARCHITECTED_PILLAR_MATRIX.md",
        "security/THREAT_MODEL.md": "THREAT_MODEL.md",
        "ops/RUNBOOK.md": "OPERATIONS_MODEL.md",
        "c4/DIAGRAM_GUIDE.md": "DIAGRAM_GUIDE.md",
    }

    for rel_path, dest_name in template_map.items():
        template_path = templates_base / rel_path
        dest_path = arch_docs_dir / dest_name

        if template_path.exists():
            if not dest_path.exists() or dest_path.stat().st_size == 0:
                shutil.copy2(template_path, dest_path)
                print(f"✓ Created: {dest_path}")
            else:
                print(f"! Skipping existing file: {dest_path}")
        else:
            print(f"! Template not found: {template_path}")

    # Handle Service Specs from Registry
    service_catalog_path = repo_root / "registries" / "service_catalog.yml"
    if service_catalog_path.exists():
        catalog_content = service_catalog_path.read_text()
        catalog = parse_simple_yaml(catalog_content)
        services = catalog.get("services", [])

        service_template_path = templates_base / "service" / "SERVICE_SPEC.md"

        for svc in services:
            svc_id = svc.get("id", "UNKNOWN")
            svc_name = svc.get("name", "Unknown Service")
            dest_path = services_dir / f"{svc_id}.md"

            if not dest_path.exists() or dest_path.stat().st_size == 0:
                content = f"# Service Specification: {svc_name}\n\n"
                content += f"- **ID**: {svc_id}\n"
                content += f"- **Type**: {svc.get('type', 'N/A')}\n"
                content += f"- **Description**: {svc.get('description', 'N/A')}\n"
                content += f"- **Owner**: {svc.get('owner_role', 'N/A')}\n\n"
                content += "## Interface\n- TBD\n\n## Dependencies\n- TBD\n"

                dest_path.write_text(content)
                print(f"✓ Generated service spec: {dest_path}")

    # Initialize Index
    # We will call update_indexes.py separately or implement it here
    print("\nArchitecture scaffolding complete.")

def main():
    parser = argparse.ArgumentParser(description="Scaffold architecture documentation.")
    parser.add_argument("--target", type=str, default=".", help="Target directory (default: current)")
    args = parser.parse_args()

    scaffold_docs(Path(args.target))

if __name__ == "__main__":
    main()
