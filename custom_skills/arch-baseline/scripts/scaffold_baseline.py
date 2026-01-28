#!/usr/bin/env python3
"""
Scaffold Baseline
Initializes a new project baseline from templates.
"""

import argparse
import json
import os
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path


def scaffold_baseline(target_dir: Path):
    """Scaffold a new project baseline."""
    print(f"Scaffolding baseline in: {target_dir}")

    # Define paths
    repo_root = Path(__file__).parent.parent.parent.parent
    templates_dir = repo_root / "custom_skills" / "arch-baseline" / "resources" / "templates" / "baseline"
    baseline_docs_dir = target_dir / "docs" / "baseline"
    registries_dir = target_dir / "registries"
    audit_dir = target_dir / "docs" / "audit"
    golden_templates_dir = baseline_docs_dir / "golden_templates"

    # 1. Create directory structure
    for d in [baseline_docs_dir, registries_dir, audit_dir, golden_templates_dir,
              audit_dir / "evidence", audit_dir / "tool_calls"]:
        d.mkdir(parents=True, exist_ok=True)
        print(f"✓ Created directory: {d}")

    # 2. Copy templates to docs/baseline/
    if templates_dir.exists():
        for template in templates_dir.glob("*.md"):
            dest = baseline_docs_dir / template.name
            if not dest.exists():
                shutil.copy2(template, dest)
                print(f"✓ Copied template: {template.name} -> {dest}")
            else:
                print(f"! Skipping existing file: {dest}")
    else:
        print(f"✗ Templates directory not found: {templates_dir}")

    # 3. Create mandatory governance docs if missing
    for doc in ["DOCS_GOVERNANCE.md", "ADR_POLICY.md", "BASELINE_INDEX.md", "BASELINE_HANDOFF.md"]:
        dest = baseline_docs_dir / doc
        if not dest.exists():
            dest.write_text(f"# {doc.replace('.md', '').replace('_', ' ').title()}\n\nInitialized from scaffold.\n")
            print(f"✓ Created stub: {dest}")

    # 4. Create mandatory audit logs if missing
    (audit_dir / "EVIDENCE_LOG.md").touch(exist_ok=True)
    (audit_dir / "evidence" / "evidence_log.jsonl").touch(exist_ok=True)
    (audit_dir / "tool_calls" / "tool_call_audit.jsonl").touch(exist_ok=True)
    (audit_dir / "tool_calls" / "TOOL_CALL_AUDIT_SUMMARY.md").touch(exist_ok=True)
    print("✓ Initialized audit logs")

    # 5. Initialize registries if missing
    registries = {
        "constraints_registry.yml": "version: 1\nconstraints: []\n",
        "security_controls_catalog.yml": "version: 1\ncontrols: []\n",
        "slo_catalog.yml": "version: 1\nslos: []\n",
        "service_catalog.yml": "version: 1\nservices: []\n",
        "event_catalog.yml": "version: 1\nevents: []\n",
        "env_catalog.yml": "version: 1\nenvironments: []\n",
    }
    for filename, content in registries.items():
        dest = registries_dir / filename
        if not dest.exists() or dest.stat().st_size == 0:
            dest.write_text(content)
            print(f"✓ Initialized registry: {dest}")

    # 6. Initialize baseline_manifest.json
    manifest_path = baseline_docs_dir / "baseline_manifest.json"
    if not manifest_path.exists() or manifest_path.stat().st_size == 0:
        # Load schema or default manifest
        repo_manifest_path = repo_root / "docs" / "baseline" / "baseline_manifest.json"
        if repo_manifest_path.exists():
            manifest = json.loads(repo_manifest_path.read_text())
            # Reset some fields
            manifest["generated_at_utc"] = datetime.now(timezone.utc).isoformat()
            manifest["status"] = "draft"
            manifest["baseline_id"] = f"BASELINE-{datetime.now().strftime('%Y%m%d')}"
        else:
            manifest = {
                "baseline_id": f"BASELINE-{datetime.now().strftime('%Y%m%d')}",
                "baseline_version": "1.0",
                "status": "draft",
                "generated_at_utc": datetime.now(timezone.utc).isoformat(),
                "artifacts": [],
                "registries": []
            }

        manifest_path.write_text(json.dumps(manifest, indent=2))
        print(f"✓ Created manifest: {manifest_path}")

    print("\nBaseline scaffold complete.")


def main():
    parser = argparse.ArgumentParser(description="Scaffold a new architecture baseline.")
    parser.add_argument("--target", type=str, default=".", help="Target directory (default: current)")
    args = parser.parse_args()

    scaffold_baseline(Path(args.target))


if __name__ == "__main__":
    main()
