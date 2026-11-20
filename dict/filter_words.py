"""Step 2. DeepSeek thinking model as the filter.

Batches of 15 (inside the 10-20 range). The model is told to consider,
then reply short. Think-tags are stripped before the JSON parse.

On scythe (GTX 1660, 6 GB) use deepseek-r1:8b. The 32b stays on the laptop.
"""
import json
import re
import urllib.request
from pathlib import Path

PROMPT = (
    "Consider each word. Keep it only if it is a technical, scientific, "
    "mathematical, or computing term, or a plain structural word an "
    "engineer uses (loop, array, force, voltage, derivative). "
    "Drop proper names, brands, slang, place names, given names, food "
    "trends, and anything useless outside engineering. "
    "After you consider, reply with only this JSON, nothing else: "
    '{"keep": [..], "drop": [..]}. Short. No prose.'
)

def _strip_think(text: str) -> str:
    return re.sub(r"<think>.*?</think>", "", text, flags=re.S).strip()

def ask(batch: list[str], model: str, host: str) -> dict:
    payload = json.dumps({
        "model": model,
        "prompt": PROMPT + "\n\nwords: " + " ".join(batch),
        "stream": False,
        "format": "json",
    }).encode()
    req = urllib.request.Request(
        host.rstrip("/") + "/api/generate",
        data=payload,
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=300) as r:
        raw = _strip_think(json.loads(r.read()).get("response", "{}"))
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {"keep": [], "drop": batch}

def run(words: list[str], out: str = "dict/filteredwordIndex.txt",
        model: str = "deepseek-r1:8b",
        host: str = "http://127.0.0.1:11434",
        batch: int = 15) -> Path:
    kept = 0
    p = Path(out)
    p.parent.mkdir(parents=True, exist_ok=True)
    done = set(p.read_text().split()) if p.exists() else set()
    todo = [w for w in words if w not in done]
    for i in range(0, len(todo), batch):
        chunk = todo[i:i + batch]
        res = ask(chunk, model, host)
        keep = [w for w in res.get("keep", []) if w in chunk]
        with p.open("a") as f:
            for w in keep:
                f.write(w + "\n")
        kept += len(keep)
        print(f"{i + len(chunk)}/{len(todo)} kept {kept}")
    return p
