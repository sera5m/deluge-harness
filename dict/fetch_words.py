"""Step 1. Pull a full English word list.

Source: dwyl/english-words words_alpha.txt (~370k alphabetic words).
Not definitions. Just the index the filter will cut.
"""
import urllib.request
from pathlib import Path

URL = "https://raw.githubusercontent.com/dwyl/english-words/master/words_alpha.txt"

def fetch(out: str = "dict/words_alpha.txt") -> Path:
    p = Path(out)
    p.parent.mkdir(parents=True, exist_ok=True)
    if p.exists() and p.stat().st_size > 1000:
        return p
    urllib.request.urlretrieve(URL, p)
    return p

def load(path: str = "dict/words_alpha.txt") -> list[str]:
    return [w.strip().lower() for w in Path(path).read_text().splitlines() if w.strip()]

if __name__ == "__main__":
    p = fetch()
    print(p, len(load(str(p))))
