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
        # Pre-seed weights for Law (Q1 baseline)
        seed_data = [
            ('Law', 'all', 'pdf', 'all', 0.6, 1),
            ('Law', 'all', 'pptx', 'all', 0.3, 1),
            ('Law', 'all', 'html', 'all', 0.1, 1),
            ('Science', 'all', 'pdf', 'all', 0.33, 1),
            ('Science', 'all', 'pptx', 'all', 0.33, 1),
            ('Science', 'all', 'html', 'all', 0.33, 1)
        ]
        cursor.executemany("""
            INSERT OR IGNORE INTO effectiveness (domain, audience, format, asset_type, score, count)
            VALUES (?, ?, ?, ?, ?, ?)
        """, seed_data)
        conn.commit()
        conn.close()

    def select_output_formats(self, domain: str, audience: str, accessibility_needs: Optional[List[str]] = None) -> List[OutputFormat]:
        """
        Selects top 2 output formats based on effectiveness history.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Priority for accessibility
        if accessibility_needs:
            if "blind" in accessibility_needs:
                return [OutputFormat.HTML, OutputFormat.MP3]

        cursor.execute("""
            SELECT format FROM effectiveness
            WHERE (audience = ? OR audience = 'all') AND (domain = ? OR domain = 'all')
            ORDER BY score DESC LIMIT 2
        """, (audience, domain))
        results = cursor.fetchall()
        conn.close()

        if not results:
            return [OutputFormat.PDF, OutputFormat.PPTX]

        try:
            return [OutputFormat(r[0]) for r in results]
        except ValueError:
            return [OutputFormat.PDF, OutputFormat.PPTX]

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
