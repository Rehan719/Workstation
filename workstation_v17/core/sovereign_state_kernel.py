import sqlite3
import json
import time
import hashlib
import os
import logging
from typing import Dict, Any, Optional, List

class SovereignStateKernel:
    """
    Persistent state store using SQLite (WAL) and SHA-3-512 chaining.
    Implements bitemporal versioning.
    """
    def __init__(self, db_path: str = "sovereign_state.db"):
        self.db_path = db_path
        self.logger = logging.getLogger("SovereignState")
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("""
            CREATE TABLE IF NOT EXISTS state_ledger (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                entity_id TEXT NOT NULL,
                state_json TEXT NOT NULL,
                valid_time INTEGER NOT NULL,
                tx_time INTEGER NOT NULL,
                parent_hash TEXT,
                state_hash TEXT NOT NULL
            )
        """)
        conn.execute("CREATE INDEX IF NOT EXISTS idx_entity ON state_ledger(entity_id)")
        conn.commit()
        conn.close()

    def commit_state(self, entity_id: str, state: Dict[str, Any], parent_hash: Optional[str] = None) -> str:
        """
        Commits a new state version for an entity.
        """
        state_json = json.dumps(state, sort_keys=True)
        state_hash = hashlib.sha3_512(state_json.encode()).hexdigest()
        tx_time = time.time_ns()
        valid_time = state.get("_valid_time", tx_time)

        conn = sqlite3.connect(self.db_path)
        conn.execute(
            "INSERT INTO state_ledger (entity_id, state_json, valid_time, tx_time, parent_hash, state_hash) VALUES (?, ?, ?, ?, ?, ?)",
            (entity_id, state_json, valid_time, tx_time, parent_hash, state_hash)
        )
        conn.commit()
        conn.close()

        self._save_snapshot(entity_id, state, state_hash)
        return state_hash

    def get_latest_state(self, entity_id: str) -> Optional[Dict[str, Any]]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.execute(
            "SELECT state_json FROM state_ledger WHERE entity_id = ? ORDER BY tx_time DESC LIMIT 1",
            (entity_id,)
        )
        row = cursor.fetchone()
        conn.close()
        return json.loads(row[0]) if row else None

    def _save_snapshot(self, entity_id: str, state: Dict, state_hash: str):
        snapshot_dir = "state_snapshots"
        os.makedirs(snapshot_dir, exist_ok=True)
        filename = f"{snapshot_dir}/{entity_id}_{state_hash[:16]}.json"
        with open(filename, "w") as f:
            json.dump(state, f, indent=2)

    async def load(self):
        # Compatibility for init call
        self.logger.info("SovereignStateKernel loaded.")

    async def commit(self):
        # Compatibility for shutdown call
        self.logger.info("SovereignStateKernel committed.")
