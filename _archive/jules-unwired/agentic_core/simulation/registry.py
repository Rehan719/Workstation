import logging
import sqlite3
import json
from typing import Dict, Any, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class TwinRegistry:
    """
    ARTICLE 306: Twin Registry.
    Maintains the state and versioning of all active digital twins.
    """
    def __init__(self, db_path: str = "meta/twins.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS digital_twins (
                twin_id TEXT PRIMARY KEY,
                reactor_id TEXT,
                state_json TEXT,
                version INTEGER,
                fidelity_score REAL,
                last_updated TEXT
            )
        """)
        conn.commit()
        conn.close()

    def register_twin(self, twin_id: str, reactor_id: str, initial_state: Dict[str, Any]) -> bool:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT OR REPLACE INTO digital_twins (twin_id, reactor_id, state_json, version, fidelity_score, last_updated)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (twin_id, reactor_id, json.dumps(initial_state), 1, 0.0, datetime.now().isoformat()))
            conn.commit()
            return True
        except Exception as e:
            logger.error(f"Registry: Error registering twin {twin_id}: {e}")
            return False
        finally:
            conn.close()

    def update_twin(self, twin_id: str, state: Dict[str, Any], fidelity: float):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT version FROM digital_twins WHERE twin_id = ?", (twin_id,))
        row = cursor.fetchone()
        new_version = (row[0] + 1) if row else 1

        cursor.execute("""
            UPDATE digital_twins
            SET state_json = ?, version = ?, fidelity_score = ?, last_updated = ?
            WHERE twin_id = ?
        """, (json.dumps(state), new_version, fidelity, datetime.now().isoformat(), twin_id))
        conn.commit()
        conn.close()

    def get_twin(self, twin_id: str) -> Optional[Dict[str, Any]]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM digital_twins WHERE twin_id = ?", (twin_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return {
                "twin_id": row[0],
                "reactor_id": row[1],
                "state": json.loads(row[2]),
                "version": row[3],
                "fidelity": row[4],
                "timestamp": row[5]
            }
        return None
