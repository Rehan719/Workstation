import sqlite3
import os
from typing import List, Dict, Any, Optional
import numpy as np
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

    def predict_optimal_asset(self, domain: str, audience: str) -> str:
        """
        Predicts optimal asset type using a statistical model (Truth V).
        """
        from sklearn.linear_model import LinearRegression

        # 1. Fetch historical data
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT asset_type, score FROM effectiveness WHERE domain = ? OR audience = ?", (domain, audience))
        data = cursor.fetchall()
        conn.close()

        if len(data) < 5:
            return "infographic" # Default

        # 2. Simple Linear Regression on scores (Mocked features)
        # In a real scenario, features would be multidimensional
        X = np.arange(len(data)).reshape(-1, 1)
        y = np.array([d[1] for d in data])

        model = LinearRegression().fit(X, y)

        # Predict improvement trend
        next_index = np.array([[len(data)]])
        predicted_trend = model.predict(next_index)[0]

        # Select asset type that maximizes predicted score based on segment trends
        asset_types = list(set([d[0] for d in data]))
        best_asset = asset_types[0]
        max_pred = -1.0

        for a_type in asset_types:
            a_data = [d[1] for d in data if d[0] == a_type]
            if not a_data:
                continue
            # Fit sub-model for this asset type
            a_X = np.arange(len(a_data)).reshape(-1, 1)
            a_y = np.array(a_data)
            a_model = LinearRegression().fit(a_X, a_y)
            a_pred = a_model.predict(np.array([[len(a_data)]]))[0]

            if a_pred > max_pred:
                max_pred = a_pred
                best_asset = a_type

        return best_asset

    def select_output_formats(self, domain: str, audience: str, accessibility_needs: Optional[List[str]] = None) -> List[OutputFormat]:
        """
        Selects top 2 output formats based on effectiveness history and audience similarity.
        """
        # Truth V: Predictive enhancement
        predicted_asset = self.predict_optimal_asset(domain, audience)

        # Similarity Clustering (Simplified Q3 implementation)
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Priority for accessibility
        if accessibility_needs:
            if "blind" in accessibility_needs:
                return [OutputFormat.HTML, OutputFormat.MP3]

        cursor.execute("""
            SELECT format, AVG(score) as avg_score FROM effectiveness
            WHERE (audience = ? OR audience = 'all')
            GROUP BY format
            ORDER BY avg_score DESC LIMIT 2
        """, (audience,))
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
