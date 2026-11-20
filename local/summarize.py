"""Pause the chat, ask bonsai on scythe for a summary, resume."""
import json
import urllib.request

from local.roles import SUMMARIZER, SUMMARIZER_HOST

SUM_PROMPT = (
    "Summarize the following chat for a reasoner that will continue the task. "
    "Keep: the goal, decisions, open questions, file paths touched. "
    "Drop: pleasantries, repeated attempts that failed the same way. "
    "Under 200 words."
)

def summarize(turns: list[dict], model: str = SUMMARIZER,
              host: str = SUMMARIZER_HOST) -> str:
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
