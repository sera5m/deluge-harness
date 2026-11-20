"""Step 4. Definitions from a local Wiktionary extract.

Use the Kaikki English Wiktionary JSONL (pre-parsed, one JSON object
per line). Download once on scythe, then this script keeps only the
lines whose word is in filteredwordIndex and writes one file per word
under the human-readable directory.

Download (once, ~2 GB compressed):
  curl -L -o /var/cache/ikitaku/kaikki.jsonl.gz \\
    https://kaikki.org/dictionary/English/kaikki.org-dictionary-English.jsonl.gz
  gunzip /var/cache/ikitaku/kaikki.jsonl.gz
"""
import json
from pathlib import Path

def index(path: str = "dict/filteredwordIndex.txt") -> set[str]:
    return set(Path(path).read_text().split())

def trim(kaikki: str, words: set[str],
         out_dir: str = "/ikitaku_syntheticData_dictionary_humanreadable") -> int:
    d = Path(out_dir)
    d.mkdir(parents=True, exist_ok=True)
    n = 0
    with open(kaikki) as f:
        for line in f:
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                continue
            w = (obj.get("word") or "").lower()
            if w not in words:
                continue
            (d / f"{w}.json").write_text(json.dumps({
                "word": w,
                "pos": obj.get("pos"),
                "defs": [s.get("glosses", []) for s in obj.get("senses", [])],
            }, indent=2))
            n += 1
    return n

if __name__ == "__main__":
    import sys
    print(trim(sys.argv[1], index()))
