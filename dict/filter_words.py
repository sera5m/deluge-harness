"""Step 2. DeepSeek thinking model as the filter.

Batches of 15. Reply length is capped so a long think cannot hang the
run. A timeout retries twice, then the batch is logged and skipped.
Already-written words are never redone.
"""
import json
import re
import urllib.error
import urllib.request
from pathlib import Path

PROMPT = (
    "Consider each word briefly. Keep it only if it is a technical, "
    "scientific, mathematical, or computing term, or a plain structural "
    "word an engineer uses (loop, array, force, voltage, derivative). "
    "Drop proper names, brands, slang, place names, given names, food "
    "trends, and anything useless outside engineering. "
    "Then reply with only this JSON, nothing else: "
    '{"keep": [..], "drop": [..]}. Short. No prose. No long reasoning.'
)

def _strip_think(text: str) -> str:
    return re.sub(r"<think>.*?</think>", "", text, flags=re.S).strip()

def ask(batch: list[str], model: str, host: str) -> dict:
    payload = json.dumps({
        "model": model,
        "prompt": PROMPT + "\n\nwords: " + " ".join(batch),
        "stream": False,
        "format": "json",
        "options": {"num_predict": 256, "temperature": 0.2},
    }).encode()
    req = urllib.request.Request(
        host.rstrip("/") + "/api/generate",
        data=payload,
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=180) as r:
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
    skip = Path("dict/skipped.txt")
    done = set(p.read_text().split()) if p.exists() else set()
    todo = [w for w in words if w not in done]
    for i in range(0, len(todo), batch):
        chunk = todo[i:i + batch]
        res = None
        for attempt in range(3):
            try:
                res = ask(chunk, model, host)
                break
            except (TimeoutError, urllib.error.URLError) as e:
                print(f"retry {attempt + 1} {chunk[0]}.. ({e})")
        if res is None:
            with skip.open("a") as f:
                f.write(" ".join(chunk) + "\n")
            print(f"skipped {chunk[0]}..")
            continue
        keep = [w for w in res.get("keep", []) if w in chunk]
        with p.open("a") as f:
            for w in keep:
                f.write(w + "\n")
        kept += len(keep)
        print(f"{i + len(chunk)}/{len(todo)} kept {kept}")
    return p
