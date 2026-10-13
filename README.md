# Deluge Harness

Local-first multi-machine AI orchestration layer.

Master (head) stores authoritative project state, data, and task graph. Workers receive delegated context + tasks only. Nodes register by name with availability, capabilities, and storage roles.

## Architecture

- **Head (scythe)**: Always-on master. LiteLLM gateway, orchestrator, node registry, persistent state, ikitaku, dashboard, Telegram HITL.
- **Workers** (ash-laptop and others): Register via heartbeat. Receive copied context + specific tasks. Drop out cleanly when offline or paused.
- **Specialists**: ikitaku reasoner, future deterministic tools, vision (qwen2.5vl + optional Qwen-Image-Layered for editable layers).
- **Models**: Role-based (director, coder, vision, micro). Directors prefer freer models; sub-agents can be censored. OpenRouter fallback.

## Node registry

Nodes are named and addressable (Tailscale MagicDNS or local registry). Each node reports:

- name
- availability (online / paused / offline)
- listed availability schedule
- is_bulk_storage
- capabilities (models, organs, GPU/CPU)
- endpoint

See `nodes/` and `config/nodes.example.yaml`.

## Quick start (head)

```bash
git clone https://github.com/sera5m/deluge-harness
cd deluge-harness
# install deps, configure .env, start gateway + presence receiver + dashboard
```

## Directory layout

- `config/` — LiteLLM, node examples
- `nodes/` — node schema and registry helpers
- `orchestrator/` — task decomposition and delegation
- `organs/` — ikitaku wrapper, vision, etc.
- `notify/` — Telegram HITL
- `dashboard/` — internal HTML dashboard with node graph
- `docs/` — architecture and runbooks

## Setup model

Select one node as **head** (authoritative state + dashboard).  
All other nodes are **clients**. They report to the head via Tailscale (heartbeat + model list).

Simplified flow:
1. Install Tailscale on all machines. Join the same tailnet.
2. On the chosen head: clone this repo, configure head identity, start presence receiver + LiteLLM + dashboard.
3. On clients: run a small reporter that announces name, availability, available Ollama models, and pauses when the owner is active.
4. Head routes tasks (local models or OpenRouter free models) only to currently available clients, with careful context copying and result return.

Public so anyone can clone a client reporter. Head remains under your control.
