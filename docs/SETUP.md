# Setup — laptop + scythe

Laptop runs the director (`deepseek-r1:32b`). Scythe (GTX 1660, 6 GB,
32 GB RAM) runs Engels (`digitsflow/bonsai-8b`, 1.2 GB). They run at
the same time. A 7B is tight on that card; bonsai is the one that fits.

## On scythe (SSH in)

```bash
# ollama if missing
curl -fsSL https://ollama.com/install.sh | sh
sudo systemctl enable --now ollama

# listen on the LAN, not only localhost
sudo mkdir -p /etc/systemd/system/ollama.service.d
echo -e '[Service]\nEnvironment=OLLAMA_HOST=0.0.0.0' | \
  sudo tee /etc/systemd/system/ollama.service.d/override.conf
sudo systemctl daemon-reload
sudo systemctl restart ollama

ollama pull digitsflow/bonsai-8b:latest
```

From the laptop, confirm:

```bash
curl http://scythe:11434/api/tags
```

If `scythe` does not resolve, use the IP and set
`DELUGE_SUMMARIZER_HOST=http://<ip>:11434`.

## On the laptop

```bash
ollama pull deepseek-r1:32b

git clone https://github.com/sera5m/deluge-harness
cd deluge-harness
export DELUGE_DIRECTOR_HOST=http://127.0.0.1:11434
export DELUGE_SUMMARIZER_HOST=http://scythe:11434

python -m local.run_workload workloads/language.json --workspace ws/lang
```

Director calls stay on the laptop. Summarize and Engels calls go to
scythe. Neither waits on the other's VRAM.
