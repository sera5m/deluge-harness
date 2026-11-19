"""Pause the chat, ask bonsai for a summary, resume.

Director is deepseek-r1:32b. Summarizer is digitsflow/bonsai-8b.
After the summary, Engels compresses it to slots.
"""
import json
import urllib.request

from local.roles import SUMMARIZER

SUM_PROMPT = (
    "Summarize the following chat for a reasoner that will continue the task. "
    "Keep: the goal, decisions, open questions, file paths touched. "
    "Drop: pleasantries, repeated attempts that failed the same way. "
    "Under 200 words."
)

def summarize(turns: list[dict], model: str = SUMMARIZER,
              host: str = "http://127.0.0.1:11434") -> str:
    body = "\n".join(f"{t.get('role','?')}: {t.get('content','')}" for t in turns)
    payload = json.dumps({
        "model": model,
        "prompt": SUM_PROMPT + "\n\n" + body,
        "stream": False,
    }).encode()
    req = urllib.request.Request(
        host.rstrip("/") + "/api/generate",
        data=payload,
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read()).get("response", "").strip()

def maybe_compact(turns: list[dict], budget_chars: int = 12000,
                  keep_tail: int = 4, model: str = SUMMARIZER) -> list[dict]:
    size = sum(len(t.get("content", "")) for t in turns)
    if size <= budget_chars or len(turns) <= keep_tail + 1:
        return turns
    head, tail = turns[:-keep_tail], turns[-keep_tail:]
    summary = summarize(head, model=model)
    return [{"role": "system", "content": "summary of earlier turns:\n" + summary}] + tail
