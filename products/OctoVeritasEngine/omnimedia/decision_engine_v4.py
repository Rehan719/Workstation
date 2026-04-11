import sqlite3
import os
from typing import List, Dict, Any, Optional
import numpy as np

class OmnimediaDecisionEngineV4:
    def __init__(self, db_path: str = "outputs/v4_effectiveness.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Effectiveness table (inherited from v3)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS effectiveness (
                domain TEXT,
                audience TEXT,
                format TEXT,
                asset_type TEXT,
                pipeline TEXT,
                mode TEXT,
                score FLOAT,
                count INTEGER,
                PRIMARY KEY (domain, audience, format, asset_type, pipeline, mode)
            )
        """)

        # NEW: Immune Memory table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS immune_memory (
                signature TEXT PRIMARY KEY,
                failure_type TEXT,
                count INTEGER,
                last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                resolved BOOLEAN DEFAULT 0
            )
        """)

        conn.commit()
        conn.close()

    def record_failure(self, signature: str, failure_type: str):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO immune_memory (signature, failure_type, count)
            VALUES (?, ?, 1)
            ON CONFLICT(signature) DO UPDATE SET
                count = count + 1,
                last_seen = CURRENT_TIMESTAMP
        """, (signature, failure_type))
        conn.commit()
        conn.close()

    def get_failure_count(self, signature: str) -> int:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT count FROM immune_memory WHERE signature = ?", (signature,))
        row = cursor.fetchone()
        conn.close()
        return row[0] if row else 0

    def record_outcome(self, domain, audience, asset_type, format, pipeline, mode, feedback, success):
        # Implementation similar to v3 but on v4 DB
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO effectiveness (domain, audience, format, asset_type, pipeline, mode, score, count)
            VALUES (?, ?, ?, ?, ?, ?, ?, 1)
            ON CONFLICT(domain, audience, format, asset_type, pipeline, mode) DO UPDATE SET
                score = (score * count + ?) / (count + 1),
                count = count + 1
        """, (domain, audience, format, asset_type, pipeline, mode, feedback))
        conn.commit()
        conn.close()
