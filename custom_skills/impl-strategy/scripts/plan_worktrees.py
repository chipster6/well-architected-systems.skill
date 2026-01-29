#!/usr/bin/env python3
"""
Plan Worktrees
Generates a worktree/parallelization plan from TASK_DAG.json.
"""

import json
from pathlib import Path


def plan_worktrees():
    """Generate parallelization plan."""
    print("Planning parallel workstreams...")

    repo_root = Path(__file__).parent.parent.parent.parent
    dag_path = repo_root / "docs" / "implementation" / "TASK_DAG.json"
    worktree_plan_path = repo_root / "docs" / "implementation" / "WORKTREE_PLAN.md"

    if not dag_path.exists():
        print("✗ TASK_DAG.json missing")
        return

    with open(dag_path, 'r') as f:
        dag = json.load(f)

    tasks = dag.get("tasks", [])

    content = "# Parallel Worktree Plan\n\n"
    content += "The following tasks can be executed in parallel based on current dependencies.\n"
    content += "Each 'Stream' below represents a set of tasks that are mutually independent or share the same prerequisites.\n\n"

    processed_task_ids = set()
    remaining_tasks = tasks[:]
    phase_idx = 0

    while remaining_tasks:
        current_phase_tasks = []
        next_remaining = []
        for task in remaining_tasks:
            prereqs = set(task.get("prerequisites", []))
            if prereqs.issubset(processed_task_ids):
                current_phase_tasks.append(task)
            else:
                next_remaining.append(task)

        if current_phase_tasks:
            content += f"## Workstream Phase {phase_idx}\n"
            content += "These tasks have all their prerequisites met and can proceed in parallel:\n\n"
            for t in current_phase_tasks:
                content += f"- [ ] **{t['id']}**: {t['title']}\n"
                content += f"  - *Requires*: {', '.join(t['prerequisites']) or 'Start'}\n"
            content += "\n"

            for t in current_phase_tasks:
                processed_task_ids.add(t["id"])
            phase_idx += 1
        else:
            break
        remaining_tasks = next_remaining

    worktree_plan_path.write_text(content)
    print(f"✓ Generated: {worktree_plan_path}")


def main():
    plan_worktrees()


if __name__ == "__main__":
    main()
