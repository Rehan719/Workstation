import sqlite3
import os
from typing import List, Dict, Any, Optional
from .factory import OutputFormat

class OmnimediaDecisionEngine:
    def __init__(self, db_path: str = "outputs/effectiveness.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS effectiveness (
                domain TEXT,
                audience TEXT,
                format TEXT,
                asset_type TEXT,
                score FLOAT,
                count INTEGER,
                PRIMARY KEY (domain, audience, format, asset_type)
            )
        """)
        conn.commit()
        conn.close()

    def select_output_formats(self, content_type: str, audience: str, accessibility_needs: Optional[List[str]] = None) -> List[OutputFormat]:
        """
        Selects top 2 output formats based on effectiveness history.
        In Phase Q1, if no history exists, it returns PDF and PPTX as defaults.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT format FROM effectiveness
            WHERE audience = ?
            ORDER BY score DESC LIMIT 2
        """, (audience,))
        results = cursor.fetchall()
        conn.close()

        if not results:
            return [OutputFormat.PDF, OutputFormat.PPTX]

        return [OutputFormat(r[0]) for r in results]

    def record_outcome(self, domain: str, audience: str, asset_type: str, format: str, feedback: float, success: bool):
        """
        Updates effectiveness scores (Truth IX).
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Simple moving average update
        cursor.execute("""
            SELECT score, count FROM effectiveness
            WHERE domain = ? AND audience = ? AND format = ? AND asset_type = ?
        """, (domain, audience, format, asset_type))
        row = cursor.fetchone()

        if row:
            current_score, current_count = row
            new_count = current_count + 1
            # Weighted average: 80% weight to success/feedback, 20% to history if count is low
            new_score = (current_score * current_count + feedback) / new_count
            cursor.execute("""
                UPDATE effectiveness SET score = ?, count = ?
                WHERE domain = ? AND audience = ? AND format = ? AND asset_type = ?
            """, (new_score, new_count, domain, audience, format, asset_type))
        else:
            cursor.execute("""
                INSERT INTO effectiveness (domain, audience, format, asset_type, score, count)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (domain, audience, format, asset_type, feedback, 1))

        conn.commit()
        conn.close()
