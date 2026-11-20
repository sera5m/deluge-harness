"""Step 3. Copy filteredwordIndex to a backup directory."""
import shutil
from datetime import datetime
from pathlib import Path

def backup(src: str = "dict/filteredwordIndex.txt",
           dest_dir: str = "/var/backups/ikitaku") -> Path:
    d = Path(dest_dir)
    d.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d-%H%M")
    dest = d / f"filteredwordIndex-{stamp}.txt"
    shutil.copy(src, dest)
    shutil.copy(src, d / "filteredwordIndex-latest.txt")
    return dest

if __name__ == "__main__":
    print(backup())
