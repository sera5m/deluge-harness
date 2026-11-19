# Local harness

The multi-machine head/worker path is deprecated for now. One machine.
Ollama on localhost. The classification task needs a long time range, so
the harness keeps a workspace and a summary instead of a growing chat.

## Pieces

- `local/prompt.py` — load a prompt file. The system text is a file, not
  a string in the script.
- `local/workspace.py` — a small directory the model can list, read, and
  write. Nothing outside it.
- `local/summarize.py` — when the chat crosses a token budget, pause,
  call a small model, replace the middle with the summary, continue.

## Replicant, used not copied

Project Replicant (Walker-Industries-RnD, permission granted) has two
clients: a summarizer and Engels. The pattern, not the Unity code:

- summarizer: a small model, a fixed prompt, ChatML in, short text out
- Engels: structured slots (name, likes, notes) rather than free prose

We use that shape. The small model is `qwen2.5:7b` or `bonsai-8b`.
Engels slots land in the workspace as JSON, so the galaxy viewer can
read them later.

## Loop

```
load prompt
open workspace
while task not done:
    if chat over budget: pause, summarize, resume
    call model with prompt + workspace listing + summary + last turns
    if model asks for a file: read/write inside workspace only
    if model asks for a compare: call iki_think, append the reading
```

## What is not in this pass

- Tailscale, node registry, multi-machine delegation
- Telegram HITL
- the dashboard node graph

Those stay in the repo. They are not the path.
