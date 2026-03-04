import logging
import sqlite3
import os
from typing import Dict, Any, List, Optional
from agentic_core.config.loader import settings

logger = logging.getLogger(__name__)

class DatabaseManager:
    """
    ARTICLE 150: Persistent storage for Workstation metadata and telemetry.
    Supports SQLite/PostgreSQL (v99 implementation defaults to SQLite).
    """
    def __init__(self, db_url: str = settings.get("DB_URL")):
        self.db_path = db_url.replace("sqlite:///", "")
        self._init_db()

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

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

        conn.commit()
        conn.close()
        logger.info(f"DatabaseManager: Initialized at {self.db_path}")

    def save_workspace(self, ws_id: str, name: str, owner_id: str):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT OR REPLACE INTO workspaces (ws_id, name, owner_id) VALUES (?, ?, ?)", (ws_id, name, owner_id))
        conn.commit()
        conn.close()

    def log_telemetry(self, persona: str, event_type: str, success: bool):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO telemetry (persona, event_type, success) VALUES (?, ?, ?)", (persona, event_type, success))
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
