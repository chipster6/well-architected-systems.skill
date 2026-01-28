#!/usr/bin/env python3
"""
Update Indexes
Maintains architecture documentation indexes.
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

    docs = sorted([f.name for f in arch_docs_dir.glob("*.md") if f.name != "ARCHITECTURE_INDEX.md"])

    content = "# Architecture Documentation Index\n\n"
    content += "## Core Documents\n"
    for doc in docs:
        content += f"- [{doc.replace('.md', '').replace('_', ' ').title()}]({doc})\n"

    index_path.write_text(content)
    print(f"✓ Updated: {index_path}")


def main():
    update_indexes()


if __name__ == "__main__":
    main()
