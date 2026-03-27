import os
from pathlib import Path

# Base directory (repository root)
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Data directories
DATA_DIR = BASE_DIR / "data"
LOG_DIR = BASE_DIR / "logs"
GENOME_DIR = BASE_DIR / "genome"
MODELS_DIR = BASE_DIR / "models"
L7_DIR = BASE_DIR / "agentic_core" / "layers" / "l7_module_library"

# Specific file paths
MEMORY_FILE = DATA_DIR / "memory.json"
INTERACTIONS_DB = DATA_DIR / "interactions.db"
L7_REGISTRY_FILE = L7_DIR / "registry.json"
CHROMA_DB_PATH = str(DATA_DIR / "chroma_db")

def ensure_dirs():
    """Ensure all required directories exist."""
    dirs = [DATA_DIR, LOG_DIR, GENOME_DIR, MODELS_DIR, L7_DIR]
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)

ensure_dirs()
