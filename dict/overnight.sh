#!/bin/bash
# Steps 1-4 on scythe. Step 5 is unset. Step 6 is the laptop, later.
#   bash dict/overnight.sh
#   bash dict/overnight.sh --model digitsflow/bonsai-8b:latest
set -e
cd "$(dirname "$0")/.."
MODEL="${1:-deepseek-r1:8b}"
[ "$1" = "--model" ] && MODEL="$2"

echo "[1] word list"
python -m dict.fetch_words

echo "[2] filter ($MODEL)"
python -m dict.filter_words --model "$MODEL"

echo "[3] backup"
python -m dict.backup

echo "[4] wiktionary trim"
K=/var/cache/ikitaku/kaikki.org-dictionary-English.jsonl
if [ ! -f "$K" ]; then
  echo "missing $K — download the Kaikki English JSONL first"
  exit 1
fi
python -m dict.wiktionary "$K"

echo "[5] unset — stop here"
