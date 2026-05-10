import sqlite3
import datetime
import os
from agentic_core.config.paths import INTERACTIONS_DB

class InteractionLogger:
    def __init__(self):
        self.db_path = str(INTERACTIONS_DB)
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS logs
                     (timestamp TEXT, agent TEXT, user_query TEXT, ai_response TEXT, feedback INTEGER)''')
        conn.commit()
        conn.close()

    def log_interaction(self, agent, query, response, feedback=0):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("INSERT INTO logs VALUES (?, ?, ?, ?, ?)",
                  (datetime.datetime.now().isoformat(), agent, query, response, feedback))
        conn.commit()
        conn.close()

interaction_logger = InteractionLogger()
