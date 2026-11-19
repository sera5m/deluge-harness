"""System prompt is a file. Swap the file, swap the agent."""
from pathlib import Path

def load_prompt(path: str) -> str:
    return Path(path).read_text()

def render(template: str, **slots: str) -> str:
    out = template
    for k, v in slots.items():
        out = out.replace("{{" + k + "}}", v)
    return out
