#!/usr/bin/env bash
# Deluge client setup + reporter
# Usage: ./setup_client.sh scythe ash-laptop
# or:    ./setup_client.sh http://scythe:8765 my-node-name

set -e

HEAD="${1:-http://scythe:8765}"
NAME="${2:-$(hostname)}"

# if first arg looks like a hostname only, turn it into a URL
if [[ "$HEAD" != http* ]]; then
  HEAD="http://${HEAD}:8765"
fi

echo "=== Deluge client setup ==="
echo "Head: $HEAD"
echo "Name: $NAME"

# make sure python is available
if ! command -v python3 >/dev/null; then
  echo "python3 not found. Install it first."
  exit 1
fi

# optional: check ollama
if command -v ollama >/dev/null; then
  echo "Ollama found — models will be reported."
else
  echo "Ollama not found — reporter will still run but report no models."
fi

# ensure reporter is executable
chmod +x client/reporter.py 2>/dev/null || true

echo
echo "Starting reporter (Ctrl+C to stop)..."
echo "----------------------------------------"
exec python3 client/reporter.py --head "$HEAD" --name "$NAME"
