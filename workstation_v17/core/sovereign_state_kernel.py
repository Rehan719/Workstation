import sqlite3
import json
import hashlib
import logging
from typing import Dict, Any, Optional

class SovereignStateKernel:
    """Persistent state store (SQLite WAL)."""
    def __init__(self, db_path: str = "sovereign_state.db"):
        self.db_path = db_path
        self.logger = logging.getLogger("SovereignState")
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("CREATE TABLE IF NOT EXISTS state (id TEXT PRIMARY KEY, data TEXT, hash TEXT)")
        conn.commit()
        conn.close()

    async def commit_state(self, entity_id: str, state: Dict[str, Any]):
        state_json = json.dumps(state, sort_keys=True)
        state_hash = hashlib.sha3_512(state_json.encode()).hexdigest()
        conn = sqlite3.connect(self.db_path)
        conn.execute("INSERT OR REPLACE INTO state (id, data, hash) VALUES (?, ?, ?)", (entity_id, state_json, state_hash))
        conn.commit()
        conn.close()

    async def load(self):
        self.logger.info("SovereignStateKernel loaded.")

    async def commit(self):
        self.logger.info("SovereignStateKernel committed.")
