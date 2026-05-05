#!/usr/bin/env python3
"""
Update Indexes
Maintains architecture documentation indexes and cross-links.
"""

import argparse
from pathlib import Path


def update_indexes():
    """Update documentation indexes."""
    print("Updating architecture indexes...")

    repo_root = Path(__file__).parent.parent.parent.parent
    arch_docs_dir = repo_root / "docs" / "architecture"

    if not arch_docs_dir.exists():
        print("✗ Architecture docs directory missing")
        return

    index_path = arch_docs_dir / "ARCHITECTURE_INDEX.md"

    # Find all docs including those in subdirectories
    docs = sorted([f.relative_to(arch_docs_dir) for f in arch_docs_dir.rglob("*.md") if f.name != "ARCHITECTURE_INDEX.md"])

    content = "# Architecture Documentation Index\n\n"

    content += "## 1. References to Baseline (Governance)\n"
    content += "- [Baseline Index](../baseline/BASELINE_INDEX.md)\n"
    content += "- [Well-Architected Adherence Plan](../baseline/WELL_ARCHITECTED_ADHERENCE_PLAN.md)\n"
    content += "- [Constraints Registry](../../registries/constraints_registry.yml)\n\n"

    content += "## 2. Core Architecture Documents\n"
    core_docs = [d for d in docs if d.parent == Path(".")]
    for doc in core_docs:
        name = doc.name.replace('.md', '').replace('_', ' ').title()
        content += f"- [{name}]({doc})\n"

    content += "\n## 3. Service Specifications\n"
    service_docs = [d for d in docs if d.parent == Path("services")]
    if service_docs:
        for doc in service_docs:
            name = doc.name.replace('.md', '')
            content += f"- [Service Spec: {name}]({doc})\n"
    else:
        content += "- None defined yet.\n"

    index_path.write_text(content)
    print(f"✓ Updated: {index_path}")


def main():
    update_indexes()


if __name__ == "__main__":
    main()
