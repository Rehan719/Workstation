import os
import json
import sqlite3
from pathlib import Path
from agentic_core.config.paths import DATA_DIR, L7_REGISTRY_FILE, INTERACTIONS_DB, ensure_dirs

def init_data():
    print("🚀 Initializing Workstation v1.0 Production Data...")

    # 1. Ensure directories exist
    ensure_dirs()

    # 2. Initialize JSON files if missing
    files_to_init = {
        DATA_DIR / "memory.json": {},
        DATA_DIR / "meeting_log.json": [],
        L7_REGISTRY_FILE: {}
    }

    for file_path, default_content in files_to_init.items():
        if not file_path.exists():
            with open(file_path, "w") as f:
                json.dump(default_content, f, indent=2)
            print(f"✅ Created {file_path}")
        else:
            print(f"ℹ️ {file_path} already exists.")

    # 3. Initialize SQLite Database
    if not INTERACTIONS_DB.exists():
        conn = sqlite3.connect(str(INTERACTIONS_DB))
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS logs
                     (timestamp TEXT, agent TEXT, user_query TEXT, ai_response TEXT, feedback INTEGER)''')
        conn.commit()
        conn.close()
        print(f"✅ Initialized SQLite DB at {INTERACTIONS_DB}")
    else:
        print(f"ℹ️ SQLite DB already exists at {INTERACTIONS_DB}")

    print("\n🌟 Data Initialization Complete.")

if __name__ == "__main__":
    init_data()
