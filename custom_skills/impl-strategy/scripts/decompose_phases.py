#!/usr/bin/env python3
"""
Decompose Phases
Generates PHASE_PLAN.md from TASK_DAG.json.
"""

import json
from pathlib import Path


def decompose_phases():
    """Generate phase plan from task DAG."""
    print("Decomposing implementation into phases...")

    repo_root = Path(__file__).parent.parent.parent.parent
    dag_path = repo_root / "docs" / "implementation" / "TASK_DAG.json"
    phase_plan_path = repo_root / "docs" / "implementation" / "PHASE_PLAN.md"

    if not dag_path.exists():
        print("✗ TASK_DAG.json missing")
        return

    with open(dag_path, 'r') as f:
        dag = json.load(f)

    tasks = dag.get("tasks", [])

    # Simple phase grouping:
    # Phase 0: Tasks with no prerequisites
    # Phase 1: Tasks that only depend on Phase 0
    # ...

    phases = []
    processed_task_ids = set()
    remaining_tasks = tasks[:]

    while remaining_tasks:
        current_phase_tasks = []
        next_remaining = []
        for task in remaining_tasks:
            prereqs = set(task.get("prerequisites", []))
            if prereqs.issubset(processed_task_ids):
                current_phase_tasks.append(task)
            else:
                next_remaining.append(task)

        if not current_phase_tasks:
            print("✗ Cyclic dependency detected in TASK_DAG.json")
            break

        phases.append(current_phase_tasks)
        for t in current_phase_tasks:
            processed_task_ids.add(t["id"])
        remaining_tasks = next_remaining

    # Generate Markdown
    content = "# Implementation Phase Plan\n\n"
    for i, phase_tasks in enumerate(phases):
        content += f"## Phase {i}: {['Foundation', 'Execution', 'Refinement', 'Completion'][min(i, 3)]}\n"
        for task in phase_tasks:
            content += f"### {task['id']}: {task['title']}\n"
            content += f"- **Description**: {task['description']}\n"
            content += f"- **Prerequisites**: {', '.join(task['prerequisites']) or 'None'}\n"
            content += f"- **Validation**: {task['validation']}\n\n"

    phase_plan_path.write_text(content)
    print(f"✓ Generated: {phase_plan_path}")


def main():
    decompose_phases()


if __name__ == "__main__":
    main()
