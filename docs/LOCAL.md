# Local harness

The multi-machine head/worker path is deprecated for now. One machine.
Ollama on localhost.

## Roles

- Director: `deepseek-r1:32b`. Does the work.
- Summarizer: `digitsflow/bonsai-8b:latest`. Pauses the chat, writes a
  short summary, then Engels compresses that summary to slots.

## Pieces

- `local/roles.py` — the two model names.
- `local/prompt.py` — system text is a file.
- `local/workspace.py` — list/read/write inside one directory.
- `local/summarize.py` — pause, bonsai summarizes, keep the tail.
- `local/engels.py` — summary → JSON slots (`goal`, `decisions`, `open`,
  `files`, `next`). Written into the workspace.
- `local/tasks.py` + `local/run_workload.py` — a workload is a list of
  steps. Each step runs, then Engels writes `engels-<id>.json`.

## Replicant, used not copied

Project Replicant has two clients: a summarizer and Engels. We use the
shape. Summarizer is bonsai. Engels slots are JSON in the workspace, so
the galaxy viewer can read them later.

## Memory spaces

Ikitaku keeps several memory files under `ikitaku-engine/memory/spaces/`.
`spaces.py` picks the active one. Each save copies the current
`graph.json` to `graph.<n>.json` first, so a bad teaching pass can be
restored.

## First workload

`workloads/language.json` builds the language file in four steps:
verbs, nouns, compositions, graph.

```bash
python -m local.run_workload workloads/language.json --workspace ws/lang
```

## What is not in this pass

- Tailscale, node registry, multi-machine delegation
- Telegram HITL
- the dashboard node graph
