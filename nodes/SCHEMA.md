# Node definition schema for Deluge Harness
# Nodes are registered by name. Head is authoritative store.
# Workers receive only delegated context + tasks.

node:
  name: string          # unique, DNS-safe (e.g. scythe, ash-laptop)
  hostname: string      # Tailscale or local name for access
  ip: string            # last known
  role: string          # head | worker | specialist
  availability: enum    # online | paused | offline
  listed_availability: string  # e.g. "24/7", "evenings", "when idle"
  is_bulk_storage: bool # true if this node holds large datasets / models cache
  capabilities:
    models: list[string]
    organs: list[string]   # e.g. ["ikitaku", "vision"]
    gpu: string
    cpu: string
    ram_gb: number
  endpoint: string      # Ollama or service URL
  last_heartbeat: timestamp
  notes: string

# Delegation model:
# - Project data lives on head (scythe)
# - Orchestrator copies relevant context + task description to worker
# - Worker executes and returns structured result
# - Head merges, updates state, continues
