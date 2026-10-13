#!/usr/bin/env python3
"""
Deluge Client Reporter

Runs on a worker node. Discovers local Ollama models and heartbeats to the head.

Usage:
  python3 client/reporter.py --head http://scythe:8765 --name ash-laptop
"""

import argparse
import json
import subprocess
import time
import urllib.request
import urllib.error
import socket

def get_ollama_models():
    try:
        out = subprocess.check_output(["ollama", "list"], text=True, timeout=10)
        models = []
        for line in out.splitlines()[1:]:  # skip header
            parts = line.split()
            if parts:
                models.append(parts[0])
        return models
    except Exception:
        return []

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return ""

def send_heartbeat(head_url, payload):
    data = json.dumps(payload).encode()
    req = urllib.request.Request(
        head_url.rstrip("/") + "/heartbeat",
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.status, resp.read().decode()
    except urllib.error.URLError as e:
        return 0, str(e)

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--head", required=True, help="http://scythe:8765")
    p.add_argument("--name", required=True, help="node name")
    p.add_argument("--role", default="worker")
    p.add_argument("--interval", type=int, default=20)
    p.add_argument("--paused", action="store_true", help="mark as paused")
    args = p.parse_args()

    print(f"Reporting as {args.name} to {args.head} every {args.interval}s")

    while True:
        models = get_ollama_models()
        payload = {
            "name": args.name,
            "hostname": args.name,
            "role": args.role,
            "availability": "paused" if args.paused else "online",
            "models": models,
            "endpoint": f"http://{args.name}:11434",
            "ip": get_local_ip(),
            "notes": "client reporter",
        }
        status, body = send_heartbeat(args.head, payload)
        print(f"[{time.strftime('%H:%M:%S')}] {status} models={len(models)} {body[:80]}")
        time.sleep(args.interval)

if __name__ == "__main__":
    main()
