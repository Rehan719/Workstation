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
# W893 (FU-1168) - ONE DATA ROOT. The deployments set DATA_DIR (render.yaml, the Dockerfile, both compose files), which
# every store resolved through agentic_core.config.data_path follows, and this file read only WORKSTATION_DATA_DIR.
# So on the durable disk render.yaml describes, the memory store, the interactions database, the L7 registry, the
# meeting log and the synthesis, ingestion, CEO and QEP stores stayed in <repo>/data and were lost on a redeploy.
# WORKSTATION_DATA_DIR still wins where it is set; otherwise DATA_DIR; otherwise <root>/data, as before.
_ROOT_SET = os.environ.get("WORKSTATION_DATA_DIR") or os.environ.get("DATA_DIR")
DATA_DIR = Path(_ROOT_SET).expanduser() if _ROOT_SET else BASE_DIR / "data"
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


def _holds(p: Path):
    """What the store HOLDS, with its unit: ('entries', n) for a JSON list or object, ('bytes', n) for anything
    else (refutation 2: a byte count was once reported as an entry count, and an unreadable store here could
    mask a live legacy list). W893 - module level, so both warnings below read a store the same way."""
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


def legacy_store_warning() -> str | None:
    """W473 (FU-026) — the store is relocated by COPY, VERIFY, SWITCH (scripts/relocate_data_store.py), never
    silently. While a legacy store at <repo-parent>/data still holds MORE than the repository's, say so: the
    live memory is there, not here."""
    if os.environ.get("WORKSTATION_DATA_DIR"):
        return None
    legacy = _LEGACY_BASE / "data" / "memory.json"
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


def previous_root_warning() -> str | None:
    """W893 (FU-1168) - never a silent switch (W473's rule). Before W893 this file followed only WORKSTATION_DATA_DIR,
    so where DATA_DIR alone was set these stores were kept in <root>/data. They now follow DATA_DIR. While <root>/data
    still holds a memory store richer than the one under DATA_DIR, say so: the memory is there, not here."""
    if os.environ.get("WORKSTATION_DATA_DIR") or not os.environ.get("DATA_DIR"):
        return None
    before = BASE_DIR / "data" / "memory.json"
    try:
        if not before.exists() or before.resolve() == Path(MEMORY_FILE).resolve():
            return None
        was_u, was = _holds(before)
        now_u, now = _holds(MEMORY_FILE) if Path(MEMORY_FILE).exists() else ("entries", 0)
        #  relocate_data_store.py copies from <repo-parent>/data only, so it is not named here
        hint = (f"copy the stores in {before.parent} into {Path(MEMORY_FILE).parent} and verify them before relying "
                f"on this location, or set WORKSTATION_DATA_DIR={before.parent} to keep them where they were")
        if was_u != now_u:
            return (f"the AI memory store at {before} ({was:,} {was_u}) cannot be compared with {MEMORY_FILE} "
                    f"({now:,} {now_u}): one of them is not a JSON store — {hint}")
        if was > now:
            return (f"the AI memory store at {before} holds {was:,} {was_u} against {now:,} at {MEMORY_FILE}, "
                    f"which DATA_DIR names since W893 — {hint}")
    except OSError:
        return None
    return None


ensure_dirs()
for _warn in (legacy_store_warning(), previous_root_warning()):
    if _warn:
        logging.getLogger("config.paths").warning(_warn)
