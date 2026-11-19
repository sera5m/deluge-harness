"""A short task list for repetitive work.

A workload is a list of steps. Each step is a prompt file plus a task
string. The runner runs them in order, writing Engels slots after each,
so a long job does not depend on the chat staying in memory.
"""
import json
from pathlib import Path

def load_workload(path: str) -> list[dict]:
    return json.loads(Path(path).read_text())

def next_open(steps: list[dict]) -> dict | None:
    for s in steps:
        if s.get("status") != "done":
            return s
    return None

def mark(steps: list[dict], step_id: str, status: str) -> None:
    for s in steps:
        if s.get("id") == step_id:
            s["status"] = status

def save_workload(path: str, steps: list[dict]) -> None:
    Path(path).write_text(json.dumps(steps, indent=2))
