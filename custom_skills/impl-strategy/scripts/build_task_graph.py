#!/usr/bin/env python3
"""
Build Task Graph
Generates TASK_DAG.json from architecture documentation and registries.
"""

import argparse
import json
import os
from pathlib import Path


def build_task_graph():
    """Build the implementation task graph."""
    print("Building implementation task graph...")

    repo_root = Path(__file__).parent.parent.parent.parent
    impl_dir = repo_root / "docs" / "implementation"
    impl_dir.mkdir(parents=True, exist_ok=True)

    # Representative tasks
    tasks = [
        {
            "id": "TASK-0001",
            "title": "Infrastructure Setup",
            "description": "Initialize cloud environment based on baseline provider selection.",
            "prerequisites": [],
            "outputs": ["env_ready"],
            "validation": "Check provider console/CLI for resources.",
            "acceptance_criteria": "VPC/Network and IAM roles exist."
        },
        {
            "id": "TASK-0002",
            "title": "Core API Implementation",
            "description": "Develop core API services as defined in SERVICE_CATALOG.md.",
            "prerequisites": ["TASK-0001"],
            "outputs": ["api_deployed"],
            "validation": "Run integration tests against dev endpoint.",
            "acceptance_criteria": "API returns 200 OK for health check."
        },
        {
            "id": "TASK-0003",
            "title": "Security Hardening",
            "description": "Apply security controls from THREAT_MODEL.md.",
            "prerequisites": ["TASK-0001"],
            "outputs": ["security_hardened"],
            "validation": "Run security scanning tool.",
            "acceptance_criteria": "Zero high-critical vulnerabilities."
        },
        {
            "id": "TASK-0004",
            "title": "Production Readiness",
            "description": "Finalize operations model and monitoring.",
            "prerequisites": ["TASK-0002", "TASK-0003"],
            "outputs": ["prod_ready"],
            "validation": "Run production readiness checklist.",
            "acceptance_criteria": "SLOs are configured and monitored."
        }
    ]

    dag = {
        "version": "1.0",
        "tasks": tasks,
        "metadata": {
            "generated_at": os.popen("date -u +%Y-%m-%dT%H:%M:%SZ").read().strip()
        }
    }

    dag_path = impl_dir / "TASK_DAG.json"
    with open(dag_path, 'w') as f:
        json.dump(dag, f, indent=2)

    print(f"✓ Generated: {dag_path}")


def main():
    build_task_graph()


if __name__ == "__main__":
    main()
