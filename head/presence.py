#!/usr/bin/env python3
"""
Deluge Head Presence Receiver

Accepts heartbeats from client nodes, stores node state, and serves the registry.
Run on the head (scythe). Clients POST to /heartbeat.

Usage:
  python3 head/presence.py --port 8765
"""

import json
import os
import argparse
from datetime import datetime, timezone
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse

REGISTRY_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "nodes.json")
os.makedirs(os.path.dirname(REGISTRY_PATH), exist_ok=True)

def load_registry():
    if os.path.exists(REGISTRY_PATH):
        try:
            with open(REGISTRY_PATH) as f:
                return json.load(f)
        except Exception:
            pass
    return {"nodes": {}, "updated": None}

def save_registry(reg):
    reg["updated"] = datetime.now(timezone.utc).isoformat()
    with open(REGISTRY_PATH, "w") as f:
        json.dump(reg, f, indent=2)

class Handler(BaseHTTPRequestHandler):
    def _send(self, code, body, content_type="application/json"):
        data = body.encode() if isinstance(body, str) else json.dumps(body).encode()
        self.send_response(code)
        self.send_header("Content-Type", content_type)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        path = urlparse(self.path).path
        reg = load_registry()
        if path in ("/", "/nodes", "/registry"):
            self._send(200, reg)
        elif path == "/health":
            self._send(200, {"status": "ok", "nodes": len(reg.get("nodes", {}))})
        else:
            self._send(404, {"error": "not found"})

    def do_POST(self):
        path = urlparse(self.path).path
        if path != "/heartbeat":
            self._send(404, {"error": "not found"})
            return

        length = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(length)
        try:
            payload = json.loads(raw.decode())
        except Exception as e:
            self._send(400, {"error": f"bad json: {e}"})
            return

        name = payload.get("name")
        if not name:
            self._send(400, {"error": "missing name"})
            return

        reg = load_registry()
        nodes = reg.setdefault("nodes", {})
        nodes[name] = {
            "name": name,
            "hostname": payload.get("hostname", name),
            "role": payload.get("role", "worker"),
            "availability": payload.get("availability", "online"),
            "listed_availability": payload.get("listed_availability", ""),
            "is_bulk_storage": bool(payload.get("is_bulk_storage", False)),
            "models": payload.get("models", []),
            "organs": payload.get("organs", []),
            "gpu": payload.get("gpu", ""),
            "cpu": payload.get("cpu", ""),
            "ram_gb": payload.get("ram_gb", 0),
            "endpoint": payload.get("endpoint", ""),
            "last_heartbeat": datetime.now(timezone.utc).isoformat(),
            "notes": payload.get("notes", ""),
            "ip": payload.get("ip", ""),
        }
        save_registry(reg)
        self._send(200, {"ok": True, "name": name})

    def log_message(self, fmt, *args):
        print(f"[presence] {self.address_string()} {fmt % args}")

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--port", type=int, default=8765)
    p.add_argument("--bind", default="0.0.0.0")
    args = p.parse_args()
    server = HTTPServer((args.bind, args.port), Handler)
    print(f"Deluge presence receiver on http://{args.bind}:{args.port}")
    print(f"Registry: {REGISTRY_PATH}")
    print("POST /heartbeat  |  GET /nodes")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nstopped")

if __name__ == "__main__":
    main()
