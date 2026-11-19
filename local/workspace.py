"""A small filesystem the model can see. Nothing outside root."""
from pathlib import Path

class Workspace:
    def __init__(self, root: str):
        self.root = Path(root).resolve()
        self.root.mkdir(parents=True, exist_ok=True)

    def _safe(self, rel: str) -> Path:
        p = (self.root / rel).resolve()
        if not str(p).startswith(str(self.root)):
            raise ValueError("outside workspace")
        return p

    def list(self, rel: str = ".") -> list[str]:
        p = self._safe(rel)
        if not p.is_dir():
            return []
        return sorted(str(c.relative_to(self.root)) for c in p.iterdir())

    def read(self, rel: str, limit: int = 8000) -> str:
        p = self._safe(rel)
        if not p.is_file():
            return ""
        return p.read_text(errors="replace")[:limit]

    def write(self, rel: str, text: str) -> None:
        p = self._safe(rel)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text)

    def listing(self) -> str:
        lines = ["workspace:"]
        for p in sorted(self.root.rglob("*")):
            if p.is_file():
                lines.append("  " + str(p.relative_to(self.root)))
        return "\n".join(lines)
