"""One-machine loop. Deprecates the multi-machine path for this task.

Usage:
  python -m local.loop --prompt prompts/classify.txt --workspace ws/ --task "..."
"""
import argparse
import json
import subprocess
import urllib.request
from pathlib import Path

from local.prompt import load_prompt, render
from local.summarize import maybe_compact
from local.workspace import Workspace

def call_ollama(model: str, prompt: str, host: str = "http://127.0.0.1:11434") -> str:
    payload = json.dumps({"model": model, "prompt": prompt, "stream": False}).encode()
    req = urllib.request.Request(
        host.rstrip("/") + "/api/generate",
        data=payload,
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=180) as r:
        return json.loads(r.read()).get("response", "").strip()

def iki(text: str) -> str:
    try:
        out = subprocess.run(["iki_think", text], capture_output=True, text=True, timeout=30)
        return out.stdout.strip() or out.stderr.strip()
    except FileNotFoundError:
        return "(iki_think not on PATH)"

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--prompt", required=True)
    ap.add_argument("--workspace", default="ws")
    ap.add_argument("--task", required=True)
    ap.add_argument("--model", default="qwen2.5:7b")
    ap.add_argument("--turns", type=int, default=6)
    args = ap.parse_args()

    ws = Workspace(args.workspace)
    system = render(load_prompt(args.prompt), workspace=ws.listing(), task=args.task)
    turns = [{"role": "system", "content": system}, {"role": "user", "content": args.task}]

    for _ in range(args.turns):
        turns = maybe_compact(turns)
        prompt = "\n".join(f"{t['role']}: {t['content']}" for t in turns)
        reply = call_ollama(args.model, prompt)
        turns.append({"role": "assistant", "content": reply})
        print(reply)
        print("---")
        if "IKI:" in reply:
            q = reply.split("IKI:", 1)[1].strip().splitlines()[0]
            reading = iki(q)
            turns.append({"role": "tool", "content": reading})
            print(reading)
        if "DONE" in reply:
            break

if __name__ == "__main__":
    main()
