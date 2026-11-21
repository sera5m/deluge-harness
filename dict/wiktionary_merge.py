"""Merge the per-word Wiktionary files into one JSON dictionary.

  python -m dict.wiktionary_merge
  python -m dict.wiktionary_merge --src /ikitaku_syntheticData_dictionary_humanreadable --out dict/dictionary.json

Input is one <word>.json per file, as written by dict/wiktionary.py.
Output is one object keyed by word.
"""
import argparse
import json
from pathlib import Path

def merge(src: str, out: str) -> Path:
    d = Path(src)
    bag = {}
    for p in sorted(d.glob("*.json")):
        try:
            obj = json.loads(p.read_text())
        except json.JSONDecodeError:
            continue
        w = obj.get("word") or p.stem
        bag[w] = obj
    dest = Path(out)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(bag, indent=2))
    print(f"{len(bag)} entries -> {dest}")
    return dest

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default="/ikitaku_syntheticData_dictionary_humanreadable")
    ap.add_argument("--out", default="dict/dictionary.json")
    args = ap.parse_args()
    merge(args.src, args.out)

if __name__ == "__main__":
    main()
