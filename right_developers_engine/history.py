import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class HistoryEntry:
    entry_id: str
    status: str
    canonical_concept: str


class History:
    def __init__(self, entries: list[HistoryEntry]):
        self.entries = entries


def append_history_entry(path: Path, entry: HistoryEntry) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(asdict(entry), sort_keys=True) + "\n")


def read_history(path: Path) -> list[HistoryEntry]:
    if not path.exists():
        return []
    return [HistoryEntry(**json.loads(line)) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
