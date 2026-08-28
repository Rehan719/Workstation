import sqlite3
import datetime
import os
from config.paths import INTERACTIONS_DB

class InteractionLogger:
    def __init__(self):
        self.db_path = str(INTERACTIONS_DB)
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS logs
                     (timestamp TEXT, agent TEXT, user_query TEXT, ai_response TEXT, feedback INTEGER)''')
        # §17.5 invariant 1 (W333) — the interaction log is the third tenant-blind store (parallel
        # to VectorMemory + memory_v01); stamp the owning tenant so it is never a cross-tenant read
        # surface. Added idempotently to the existing table (older DBs gain the column, NULL = legacy).
        cols = {r[1] for r in c.execute("PRAGMA table_info(logs)").fetchall()}
        if "owner_id" not in cols:
            c.execute("ALTER TABLE logs ADD COLUMN owner_id TEXT")
        conn.commit()
        conn.close()

    def log_interaction(self, agent, query, response, feedback=0, owner_id=None):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("INSERT INTO logs (timestamp, agent, user_query, ai_response, feedback, owner_id) "
                  "VALUES (?, ?, ?, ?, ?, ?)",
                  (datetime.datetime.now().isoformat(), agent, query, response, feedback, owner_id))
        conn.commit()
        conn.close()

interaction_logger = InteractionLogger()
