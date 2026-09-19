import logging
import os
from pathlib import Path

# Base directory (repository root). W473 (register FU-026): this used to be `.parent.parent.parent` — the
# repository's PARENT — so without WORKSTATION_DATA_DIR the live memory store, the interactions database,
# the L7 registry, the meeting log and the chroma store lived one level above the repository, and
# ensure_dirs() created logs/genome/models directories there at import.
BASE_DIR = Path(__file__).resolve().parent.parent
_LEGACY_BASE = BASE_DIR.parent

# Data directories — WORKSTATION_DATA_DIR overrides the data root (test isolation / deployments that
# keep mutable state off the repo volume). Defaults to <root>/data so existing setups are unchanged.
DATA_DIR = Path(os.environ["WORKSTATION_DATA_DIR"]).expanduser() if os.environ.get("WORKSTATION_DATA_DIR") else BASE_DIR / "data"
LOG_DIR = BASE_DIR / "logs"
GENOME_DIR = BASE_DIR / "genome"
MODELS_DIR = BASE_DIR / "models"
L7_DIR = BASE_DIR / "agentic_core" / "layers" / "l7_module_library"

# Specific file paths (Unified in root data/ directory)
MEMORY_FILE = DATA_DIR / "memory.json"
INTERACTIONS_DB = DATA_DIR / "interactions.db"
L7_REGISTRY_FILE = DATA_DIR / "l7_registry.json"
MEETING_LOG_FILE = DATA_DIR / "meeting_log.json"
CHROMA_DB_PATH = str(DATA_DIR / "chroma_db")

def ensure_dirs():
    """Ensure all required directories exist. W473 (refutation) — at import only the DATA root is made; a bare import
    of the validator or the genome engine used to create genome/, models/, logs/ and the L7 directory inside the
    repository (they are ignored by git now, but a directory a module never writes is not made on its behalf)."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def ensure_dir(path: Path) -> Path:
    """The directory a writer is about to use, made on demand."""
    Path(path).mkdir(parents=True, exist_ok=True)
    return Path(path)


def legacy_store_warning() -> str | None:
    """W473 (FU-026) — the store is relocated by COPY, VERIFY, SWITCH (scripts/relocate_data_store.py), never
    silently. While a legacy store at <repo-parent>/data still holds MORE than the repository's, say so: the
    live memory is there, not here."""
    if os.environ.get("WORKSTATION_DATA_DIR"):
        return None
    legacy = _LEGACY_BASE / "data" / "memory.json"

    def _holds(p: Path):
        """What the store HOLDS, with its unit: ('entries', n) for a JSON list or object, ('bytes', n) for anything
        else (refutation 2: a byte count was once reported as an entry count, and an unreadable store here could
        mask a live legacy list)."""
        try:
            import json
            d = json.loads(p.read_text(encoding="utf-8"))
            if isinstance(d, (list, dict)):
                return "entries", len(d)
        except Exception:
            pass
        try:
            return "bytes", p.stat().st_size
        except OSError:
            return "bytes", 0
    try:
        if not legacy.exists():
            return None
        have_u, have = _holds(legacy)
        here_u, here = _holds(MEMORY_FILE) if MEMORY_FILE.exists() else ("entries", 0)
        hint = ("run python scripts/relocate_data_store.py to copy and verify it (a list is never merged by rule; the "
                "report says which copy is richer) before relying on this location")
        if have_u != here_u:
            return (f"the AI memory store at {legacy} ({have:,} {have_u}) cannot be compared with {MEMORY_FILE} "
                    f"({here:,} {here_u}): one of them is not a JSON store — {hint}")
        if have > here:
            return f"the AI memory store at {legacy} holds {have:,} {have_u} against {here:,} at {MEMORY_FILE} — {hint}"
    except OSError:
        return None
    return None


ensure_dirs()
_warn = legacy_store_warning()
if _warn:
    logging.getLogger("config.paths").warning(_warn)
