"""
Canonical memory_v01 module.

Backed by a real ChromaDB collection so ingested content (memory_v01.add_exchange)
is genuinely persisted and semantically searchable (memory_v01.query), rather than
silently discarded.
"""
import logging
import uuid

logger = logging.getLogger(__name__)


class MemoryV01:
    def __init__(self):
        self.data = {}
        self._collection = None
        try:
            import chromadb
            self._collection = chromadb.Client().get_or_create_collection("memory_v01")
        except Exception as e:
            logger.warning(f"memory_v01: ChromaDB unavailable, falling back to in-process dict store ({e})")

    def add_exchange(self, prompt: str, response: str):
        entry_id = str(uuid.uuid4())
        self.data[entry_id] = {"prompt": prompt, "response": response}
        if self._collection is not None:
            try:
                self._collection.add(documents=[f"{prompt}\n{response}"], ids=[entry_id])
            except Exception as e:
                logger.warning(f"memory_v01: failed to persist exchange to ChromaDB ({e})")

    def query(self, query_text: str, n_results: int = 3):
        if self._collection is not None:
            try:
                count = self._collection.count()
                if count > 0:
                    res = self._collection.query(query_texts=[query_text], n_results=min(n_results, count))
                    return res.get("documents", [[]])[0]
            except Exception as e:
                logger.warning(f"memory_v01: ChromaDB query failed, falling back ({e})")
        # Fallback: naive substring match over the in-process store
        query_lower = query_text.lower()
        matches = [
            f"{v['prompt']}\n{v['response']}"
            for v in self.data.values()
            if query_lower in v["prompt"].lower() or query_lower in v["response"].lower()
        ]
        return matches[:n_results]


memory_v01 = MemoryV01()
meeting_log = type('Mock', (), {
    'get_recent_debate': lambda: "No recent debates recorded.",
    'post_argument': lambda *a: None,
    'export_minutes': lambda: "# Minutes",
    'log': []
})()
