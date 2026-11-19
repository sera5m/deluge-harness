"""Engels: structured slots, not prose.

Pattern from Project Replicant. The summarizer writes a short text; Engels
turns that text into slots a later turn can bind. Slots land in the
workspace as JSON so the galaxy viewer can read them.
"""
import json
import urllib.request
from pathlib import Path

ENGELS_PROMPT = (
    "Turn the summary into JSON slots. Keys: goal, decisions (list), "
    "open (list), files (list), next. No prose outside the JSON."
)

def to_slots(summary: str, model: str = "digitsflow/bonsai-8b:latest",
             host: str = "http://127.0.0.1:11434") -> dict:
    payload = json.dumps({
        "model": model,
        "prompt": ENGELS_PROMPT + "\n\n" + summary,
        "stream": False,
        "format": "json",
    }).encode()
    req = urllib.request.Request(
        host.rstrip("/") + "/api/generate",
        data=payload,
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=120) as r:
        raw = json.loads(r.read()).get("response", "{}")
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {"goal": summary[:200], "decisions": [], "open": [], "files": [], "next": ""}

def write_slots(ws_root: str, slots: dict, name: str = "engels.json") -> Path:
    p = Path(ws_root) / name
    p.write_text(json.dumps(slots, indent=2))
    return p
