#!/usr/bin/env bash
# Deluge head setup
# Runs presence receiver + dashboard
# Usage: ./setup_server.sh

set -e

echo "=== Deluge head setup ==="

if ! command -v python3 >/dev/null; then
  echo "python3 not found."
  exit 1
fi

# ensure scripts are executable
chmod +x head/presence.py 2>/dev/null || true

# create data dir if missing
mkdir -p data

echo
echo "Starting presence receiver on :8765"
echo "Dashboard will be on :8080"
echo "Press Ctrl+C to stop both."
echo

# run presence in background
python3 head/presence.py --port 8765 &
PRESENCE_PID=$!

# run dashboard
python3 -m http.server 8080 --bind 0.0.0.0 --directory dashboard &
DASH_PID=$!

# cleanup on exit
cleanup() {
  echo
  echo "Stopping..."
  kill $PRESENCE_PID $DASH_PID 2>/dev/null || true
  wait
  echo "Stopped."
}
trap cleanup EXIT INT TERM

# wait
wait
