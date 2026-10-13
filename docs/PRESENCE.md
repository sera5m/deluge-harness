# Deluge Presence / Heartbeat

## Head (run on scythe)

```bash
cd deluge-harness
python3 head/presence.py --port 8765
```

Stores node state in `data/nodes.json`.  
Endpoints:
- `POST /heartbeat` — clients send their status
- `GET /nodes` — current registry
- `GET /health`

## Client (run on workers)

```bash
python3 client/reporter.py --head http://scythe:8765 --name ash-laptop
```

Discovers local `ollama list` models and reports every 20s.  
Use `--paused` to mark the node paused.

## Tailscale required

Both machines must be on the same Tailscale tailnet so `scythe` and `ash-laptop` resolve.

On EndeavourOS / Arch:

```bash
sudo pacman -S tailscale
sudo systemctl enable --now tailscaled
sudo tailscale up
# follow the auth URL
tailscale ip -4
```

Then the dashboard at `http://scythe:8080` and presence at `http://scythe:8765/nodes` are reachable from any node on the tailnet.
