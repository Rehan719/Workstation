import sqlite3
import os
from typing import List, Dict, Any, Optional
import numpy as np
from .factory import OutputFormat

class OmnimediaDecisionEngineV3:
    def __init__(self, db_path: str = "outputs/v3_effectiveness.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        # V3 Schema includes pipeline and mode
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

        # Seed logic (optional migration from v2 could go here)
        seed_data = [
            ('Law', 'all', 'pdf', 'form', 'Introspection', 'muaina', 0.9, 1),
            ('Science', 'all', 'html', 'matrix', 'Knowledge', 'jaiza', 0.85, 1)
        ]
        cursor.executemany("""
            INSERT OR IGNORE INTO effectiveness (domain, audience, format, asset_type, pipeline, mode, score, count)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, seed_data)

        conn.commit()
        conn.close()

    def predict_format(self, content_type: str, audience: str, device: str = "desktop", mode: str = "jaiza") -> str:
        """
        Truth V: Predictive format selection based on v3 dimensions.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        # Find best format for this mode and audience
        cursor.execute("""
            SELECT format FROM effectiveness
            WHERE (audience = ? OR audience = 'all') AND (mode = ? OR mode = 'all')
            ORDER BY score DESC LIMIT 1
        """, (audience, mode))
        result = cursor.fetchone()
        conn.close()

        if result:
            return result[0]
        return "html"

    def record_outcome(self,
                       domain: str,
                       audience: str,
                       asset_type: str,
                       format: str,
                       pipeline: str,
                       mode: str,
                       feedback: float,
                       success: bool):
        """
        Truth IX: Operational convergence via cross-domain learning.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT score, count FROM effectiveness
            WHERE domain = ? AND audience = ? AND format = ? AND asset_type = ? AND pipeline = ? AND mode = ?
        """, (domain, audience, format, asset_type, pipeline, mode))
        row = cursor.fetchone()

        if row:
            current_score, current_count = row
            new_count = current_count + 1
            new_score = (current_score * current_count + feedback) / new_count
            cursor.execute("""
                UPDATE effectiveness SET score = ?, count = ?
                WHERE domain = ? AND audience = ? AND format = ? AND asset_type = ? AND pipeline = ? AND mode = ?
            """, (new_score, new_count, domain, audience, format, asset_type, pipeline, mode))
        else:
            cursor.execute("""
                INSERT INTO effectiveness (domain, audience, format, asset_type, pipeline, mode, score, count)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (domain, audience, format, asset_type, pipeline, mode, feedback, 1))

        conn.commit()
        conn.close()
