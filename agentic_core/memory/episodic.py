import sqlite3
import json
from datetime import datetime
from typing import Any, Dict, List

class EpisodicMemory:
    """
    Episodic Memory: SQLite-based interaction history and event logs.
    """
    def __init__(self, db_path='episodic_memory.db'):
        self.conn = sqlite3.connect(db_path)
        self._initialize_db()

    def _initialize_db(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS episodes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_id TEXT,
                agent_id TEXT,
                timestamp DATETIME,
                event_type TEXT,
                data TEXT
            )
        ''')
        self.conn.commit()

    def add_episode(self, project_id: str, agent_id: str, event_type: str, data: Dict[str, Any]):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO episodes (project_id, agent_id, timestamp, event_type, data)
            VALUES (?, ?, ?, ?, ?)
        ''', (project_id, agent_id, datetime.utcnow().isoformat(), event_type, json.dumps(data)))
        self.conn.commit()

    def get_history(self, project_id: str) -> List[Dict[str, Any]]:
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM episodes WHERE project_id = ? ORDER BY timestamp ASC', (project_id,))
        rows = cursor.fetchall()
        return [
            {
                "id": r[0],
                "project_id": r[1],
                "agent_id": r[2],
                "timestamp": r[3],
                "event_type": r[4],
                "data": json.loads(r[5])
            } for r in rows
        ]
