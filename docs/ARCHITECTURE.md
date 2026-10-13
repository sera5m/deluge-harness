# Deluge Architecture Notes

## Head vs Workers

- Head (scythe) holds the project state, task graph, node registry, and bulk storage.
- Workers are ephemeral compute. They receive a snapshot of relevant context + a concrete task, execute, and return results.
- No shared mutable filesystem required. Delegation is explicit.

## Node naming and access

- Prefer Tailscale MagicDNS so nodes are reachable by hostname (scythe, ash-laptop).
- Harness registry maps name → current endpoint + capabilities.
- Orchestrator looks up by name or by capability when routing.

## Auto-OC on scythe (Ryzen 5 3600)

Liquid cooler present. Safest "auto" path:
1. BIOS → Enable Precision Boost Overdrive (PBO).
2. Optionally set Curve Optimizer (negative offset if stable).
3. Avoid aggressive manual all-core voltage if the machine is the always-on head.
4. Monitor temps under sustained load.

## Vision + layers

- qwen2.5vl for general vision / screenshot verification.
- Qwen-Image-Layered (when available) for decomposing images into editable RGBA layers — useful for UI verification or asset work.

## Next implementation steps

1. Presence/heartbeat receiver on head.
2. LiteLLM config that consults live node registry.
3. Simple task delegator that copies context and posts to a worker.
4. ikitaku tool wrapper.
