#!/usr/bin/env python3
"""
Update Task Status
Updates the status of a task in TASK_DAG.json.
"""

import argparse
import json
from pathlib import Path


def update_task_status(task_id: str, status: str):
    """Update task status."""
    repo_root = Path(__file__).parent.parent.parent.parent
    dag_path = repo_root / "docs" / "implementation" / "TASK_DAG.json"

    if not dag_path.exists():
        print(f"✗ {dag_path} not found")
        return

    with open(dag_path, 'r') as f:
        dag = json.load(f)

    found = False
    for task in dag.get("tasks", []):
        if task["id"] == task_id:
            task["status"] = status
            found = True
            break

    if found:
        with open(dag_path, 'w') as f:
            json.dump(dag, f, indent=2)
        print(f"✓ Updated {task_id} to {status}")
    else:
        print(f"✗ Task {task_id} not found")


def main():
    parser = argparse.ArgumentParser(description="Update task status.")
    parser.add_argument("task_id", type=str)
    parser.add_argument("status", type=str)
    args = parser.parse_args()

    update_task_status(args.task_id, args.status)


if __name__ == "__main__":
    main()
