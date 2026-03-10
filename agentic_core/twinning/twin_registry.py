import logging
import sqlite3
import os
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class TwinRegistry:
    """Manages the persistent registry of active digital twins."""
    def __init__(self, db_path: str = "meta/twins.db"):
        if db_path != ":memory:":
            os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.conn = sqlite3.connect(db_path)
        self._init_db()

    def _init_db(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS twins (
                twin_id TEXT PRIMARY KEY,
                reactor_id TEXT,
                fidelity_target REAL,
                current_fidelity REAL,
                last_sync TEXT
            )
        """)
        self.conn.commit()

    def register_twin(self, twin_id: str, reactor_id: str, fidelity_target: float):
        self.conn.execute(
            "INSERT OR REPLACE INTO twins VALUES (?, ?, ?, ?, datetime('now'))",
            (twin_id, reactor_id, fidelity_target, 1.0)
        )
        self.conn.commit()

    def get_twin(self, twin_id: str) -> Optional[Dict[str, Any]]:
        cursor = self.conn.execute("SELECT * FROM twins WHERE twin_id = ?", (twin_id,))
        row = cursor.fetchone()
        if row:
            return {
                "twin_id": row[0],
                "reactor_id": row[1],
                "fidelity_target": row[2],
                "current_fidelity": row[3]
            }
        return None
