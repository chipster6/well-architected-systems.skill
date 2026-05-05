#!/usr/bin/env python3
"""
Build Task Graph
Generates TASK_DAG.json from architecture documentation and registries.
"""

import argparse
import json
import os
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
                    current_item[k] = []
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

def build_task_graph():
    """Build the implementation task graph."""
    print("Building implementation task graph...")

    repo_root = Path(__file__).parent.parent.parent.parent
    impl_dir = repo_root / "docs" / "implementation"
    impl_dir.mkdir(parents=True, exist_ok=True)

    registries_dir = repo_root / "registries"

    tasks = []

    # Base Task
    tasks.append({
        "id": "TASK-INFRA-001",
        "title": "Cloud Foundation",
        "description": "Establish the landing zone and core network.",
        "prerequisites": [],
        "outputs": ["infrastructure_ready"],
        "validation": "Verify VPC/IAM roles via cloud CLI.",
        "acceptance_criteria": "Network and security groups exist."
    })

    # Services -> Implementation Tasks
    service_catalog = registries_dir / "service_catalog.yml"
    if service_catalog.exists():
        catalog = parse_simple_yaml(service_catalog.read_text())
        for svc in catalog.get("services", []):
            tasks.append({
                "id": f"TASK-SVC-{svc['id']}",
                "title": f"Implement {svc['name']}",
                "description": svc.get('description', 'N/A'),
                "prerequisites": ["TASK-INFRA-001"],
                "outputs": [f"{svc['name']}_deployed"],
                "validation": f"Deploy {svc['name']} and run health check.",
                "acceptance_criteria": f"{svc['name']} returns 200 OK."
            })

    # Security Controls -> Hardening Tasks
    security_catalog = registries_dir / "security_controls_catalog.yml"
    if security_catalog.exists():
        catalog = parse_simple_yaml(security_catalog.read_text())
        for ctrl in catalog.get("controls", []):
            tasks.append({
                "id": f"TASK-SEC-{ctrl['id']}",
                "title": f"Security: {ctrl['title']}",
                "description": ctrl.get('objective', 'N/A'),
                "prerequisites": ["TASK-INFRA-001"],
                "outputs": [f"control_{ctrl['id']}_applied"],
                "validation": ctrl.get('verification', 'Check security group rules.'),
                "acceptance_criteria": "Compliance scan report matches control objective."
            })

    # SLOs -> Observability Tasks
    slo_catalog = registries_dir / "slo_catalog.yml"
    if slo_catalog.exists():
        catalog = parse_simple_yaml(slo_catalog.read_text())
        for slo in catalog.get("slos", []):
            svc_task_id = f"TASK-SVC-{slo.get('service_id', 'UNKNOWN')}"
            tasks.append({
                "id": f"TASK-SLO-{slo['id']}",
                "title": f"Monitor SLO: {slo['name']}",
                "description": f"Configure SLI for {slo['name']} with target {slo.get('target', 'N/A')}.",
                "prerequisites": [svc_task_id] if any(t['id'] == svc_task_id for t in tasks) else ["TASK-INFRA-001"],
                "outputs": [f"slo_{slo['id']}_monitored"],
                "validation": "Check dashboard for SLI metrics.",
                "acceptance_criteria": f"Alerting configured for {slo['name']} threshold."
            })

    dag = {
        "version": "1.0",
        "tasks": tasks,
        "metadata": {
            "generated_at": datetime.now(timezone.utc).isoformat()
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
