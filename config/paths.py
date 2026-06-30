import os
from pathlib import Path

# Base directory (repository root)
BASE_DIR = Path(__file__).resolve().parent.parent.parent

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
    """Ensure all required directories exist."""
    dirs = [DATA_DIR, LOG_DIR, GENOME_DIR, MODELS_DIR, L7_DIR]
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)

ensure_dirs()
