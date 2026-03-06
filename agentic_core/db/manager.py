import logging
import sqlite3
import os
import json
from typing import Dict, Any, List, Optional
from agentic_core.config.loader import settings

logger = logging.getLogger(__name__)

class DatabaseManager:
    """
    ARTICLE 150: Persistent storage for Workstation metadata and telemetry.
    Supports SQLite/PostgreSQL (v99 implementation defaults to SQLite).
    """
    def __init__(self, db_url: Optional[str] = None):
        if db_url is None:
            db_url = settings.get("DB_URL", "sqlite:///jules_v99.db")
        self.db_path = db_url.replace("sqlite:///", "")
        self._init_db()

    def _get_connection(self):
        # Enable WAL mode for better concurrency (Article 150 hardening)
        conn = sqlite3.connect(self.db_path)
        conn.execute("PRAGMA journal_mode=WAL")
        return conn

    def _init_db(self):
        """Initializes database tables."""
        conn = self._get_connection()
        cursor = conn.cursor()

        # Workspace Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS workspaces (
                ws_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                owner_id TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Telemetry Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS telemetry (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                persona TEXT,
                event_type TEXT,
                success BOOLEAN,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Spiritual Metrics Table (Article 248)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS spiritual_metrics (
                user_id TEXT PRIMARY KEY,
                tazkiyah_score REAL,
                metrics_json TEXT,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Dawah Readiness Table (Article 249)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS dawah_readiness (
                user_id TEXT PRIMARY KEY,
                is_ready BOOLEAN,
                foundational_complete BOOLEAN,
                tazkiyah_threshold_passed BOOLEAN,
                character_verified BOOLEAN,
                last_evaluated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        conn.commit()
        conn.close()
        logger.info(f"DatabaseManager: Initialized at {self.db_path}")

    def save_workspace(self, ws_id: str, name: str, owner_id: str):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT OR REPLACE INTO workspaces (ws_id, name, owner_id) VALUES (?, ?, ?)", (ws_id, name, owner_id))
        conn.commit()
        conn.close()

    def log_telemetry(self, persona: str, event_type: str, success: bool, metadata: Optional[Dict[str, Any]] = None):
        """
        ARTICLE 150/247: Enhanced telemetry logging for dual-metric dashboards.
        """
        conn = self._get_connection()
        cursor = conn.cursor()

        # Ensure metadata column exists (Article 150 hardening)
        try:
            cursor.execute("ALTER TABLE telemetry ADD COLUMN metadata TEXT")
        except sqlite3.OperationalError:
            pass # Column already exists

        cursor.execute("INSERT INTO telemetry (persona, event_type, success, metadata) VALUES (?, ?, ?, ?)",
                       (persona, event_type, success, json.dumps(metadata) if metadata else None))
        conn.commit()
        conn.close()

    def get_spiritual_metrics(self, user_id: str) -> Dict[str, Any]:
        conn = self._get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM spiritual_metrics WHERE user_id = ?", (user_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            res = dict(row)
            res['metrics_json'] = json.loads(res['metrics_json'])
            return res
        return {"user_id": user_id, "tazkiyah_score": 0.0, "metrics_json": {}}

    def save_spiritual_metrics(self, user_id: str, score: float, metrics: Dict[str, Any]):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT OR REPLACE INTO spiritual_metrics (user_id, tazkiyah_score, metrics_json) VALUES (?, ?, ?)",
                       (user_id, score, json.dumps(metrics)))
        conn.commit()
        conn.close()

    def update_spiritual_metrics(self, user_id: str, metric_key: str, value: float):
        """ARTICLE 248: Incremental update for spiritual metrics."""
        current = self.get_spiritual_metrics(user_id)
        current_metrics = current['metrics_json']
        current_metrics[metric_key] = value

        # Recalculate basic score if needed or just save
        self.save_spiritual_metrics(user_id, current['tazkiyah_score'], current_metrics)

    def get_dawah_readiness(self, user_id: str) -> Dict[str, Any]:
        conn = self._get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM dawah_readiness WHERE user_id = ?", (user_id,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else {"user_id": user_id, "is_ready": False}

    def save_dawah_readiness(self, user_id: str, is_ready: bool, details: Dict[str, bool]):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO dawah_readiness
            (user_id, is_ready, foundational_complete, tazkiyah_threshold_passed, character_verified)
            VALUES (?, ?, ?, ?, ?)
        """, (user_id, is_ready, details.get('foundational', False),
              details.get('tazkiyah', False), details.get('character', False)))
        conn.commit()
        conn.close()

    def get_all_workspaces(self) -> List[Dict[str, Any]]:
        conn = self._get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM workspaces")
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
