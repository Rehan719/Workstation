import chromadb
from chromadb.config import Settings
import os
import json
import logging
from datetime import datetime
from typing import List, Dict, Any
from agentic_core.config.paths import DATA_DIR, CHROMA_DB_PATH

logger = logging.getLogger(__name__)

class SemanticMemory:
    """v0.1: Semantic Vector Store for AI CEO Long-Term Memory."""
    def __init__(self, persist_directory: str = None):
        if not persist_directory:
             persist_directory = CHROMA_DB_PATH

        os.makedirs(persist_directory, exist_ok=True)
        self.client = chromadb.PersistentClient(path=persist_directory)
        self.collection = self.client.get_or_create_collection(name="conversation_memory")

    def add_exchange(self, user_msg: str, ai_msg: str):
        """Adds an exchange to the vector store."""
        exchange_id = f"msg_{os.urandom(4).hex()}"
        metadata = {"type": "conversation", "timestamp": datetime.utcnow().isoformat()}
        self.collection.add(
            documents=[f"User: {user_msg}\nAI: {ai_msg}"],
            metadatas=[metadata],
            ids=[exchange_id]
        )
        logger.info(f"Memory: Exchange {exchange_id} added to semantic store.")

    def query(self, query_text: str, n_results: int = 2) -> List[str]:
        """Performs semantic search over past conversations."""
        try:
            results = self.collection.query(
                query_texts=[query_text],
                n_results=n_results
            )
            return results['documents'][0] if results['documents'] else []
        except Exception as e:
            logger.error(f"Memory: Query failed: {e}")
            return []

class CSuiteMeetingLog:
    """v0.1: Asynchronous Inter-Agent Meeting Log."""
    def __init__(self, log_path: str = None):
        if not log_path:
             log_path = str(DATA_DIR / "meeting_log.json")

        self.log_path = log_path
        os.makedirs(os.path.dirname(log_path), exist_ok=True)
        self.log = self._load_log()

    def _load_log(self) -> List[Dict[str, Any]]:
        if os.path.exists(self.log_path):
            try:
                with open(self.log_path, 'r') as f:
                    return json.load(f)
            except: return []
        return []

    def post_argument(self, agent: str, argument: str, vote: str = "ABSTAIN"):
        entry = {
            "agent": agent,
            "argument": argument,
            "vote": vote,
            "timestamp": datetime.utcnow().isoformat()
        }
        self.log.append(entry)
        with open(self.log_path, 'w') as f:
            json.dump(self.log, f, indent=2)

    def get_recent_debate(self) -> str:
        recent = self.log[-10:]
        return "\n".join([f"{e['agent']} ({e['vote']}): {e['argument']}" for e in recent])

    def export_minutes(self, format: str = "markdown") -> str:
        """v0.2: Export meeting minutes."""
        content = "# C-Suite Meeting Minutes\n\n"
        for e in self.log:
            content += f"### {e['agent']} ({e['vote']})\n- {e['argument']}\n- *Timestamp: {e['timestamp']}*\n\n"
        return content

memory_v01 = SemanticMemory()
meeting_log = CSuiteMeetingLog()
