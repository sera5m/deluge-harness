"""Step 2. Bonsai as a filter. Batches, not one word at a time.

Keep: technical, scientific, engineering, mathematical, computing terms.
Drop: proper names, brands, slang, food trends, place names, given names.
One word at a time would not finish overnight. Batches of 40.
"""
import json
import urllib.request
from pathlib import Path

PROMPT = (
    "You filter an English word list for an engineering reasoner. "
    "Keep a word only if it is a technical, scientific, mathematical, "
    "or computing term, or a plain structural word an engineer uses "
    "(loop, array, force, voltage, derivative). "
    "Drop proper names, brands, slang, place names, given names, "
    "food trends, and anything useless outside engineering. "
    "Reply with JSON: {\"keep\": [..], \"drop\": [..]}. No prose."
)

def ask(batch: list[str], model: str, host: str) -> dict:
    payload = json.dumps({
        "model": model,
        "prompt": PROMPT + "\n\n" + " ".join(batch),
        "stream": False,
        "format": "json",
    }).encode()
    req = urllib.request.Request(
        host.rstrip("/") + "/api/generate",
        data=payload,
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=180) as r:
        raw = json.loads(r.read()).get("response", "{}")
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {"keep": [], "drop": batch}

def run(words: list[str], out: str = "dict/filteredwordIndex.txt",
        model: str = "digitsflow/bonsai-8b:latest",
        host: str = "http://127.0.0.1:11434",
        batch: int = 40) -> Path:
    kept: list[str] = []
    p = Path(out)
    p.parent.mkdir(parents=True, exist_ok=True)
    done = set(p.read_text().split()) if p.exists() else set()
    todo = [w for w in words if w not in done]
    for i in range(0, len(todo), batch):
        chunk = todo[i:i + batch]
        res = ask(chunk, model, host)
        kept.extend(w for w in res.get("keep", []) if w in chunk)
        with p.open("a") as f:
            for w in res.get("keep", []):
                if w in chunk:
                    f.write(w + "\n")
        print(f"{i + len(chunk)}/{len(todo)} kept {len(kept)}")
    return p
