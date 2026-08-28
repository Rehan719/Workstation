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

    PLATFORM_NS = "platform"   # §17.5 invariant 1 (W343) — owner-less/shared memory namespace

    def add_exchange(self, prompt: str, response: str, owner_id: str | None = None):
        """§17.5 invariant 1 (W343) — the SECOND memory store gains the same tenancy the
        VectorMemory got in W333: every exchange is stamped with its owning namespace, so one
        tenant's avatar conversations can never be recalled into another's."""
        entry_id = str(uuid.uuid4())
        ns = owner_id or self.PLATFORM_NS
        self.data[entry_id] = {"prompt": prompt, "response": response, "owner_id": ns}
        if self._collection is not None:
            try:
                self._collection.add(documents=[f"{prompt}\n{response}"], ids=[entry_id],
                                     metadatas=[{"owner_id": ns}])
            except Exception as e:
                logger.warning(f"memory_v01: failed to persist exchange to ChromaDB ({e})")

    def query(self, query_text: str, n_results: int = 3, owner_id: str | None = None):
        allowed = [owner_id or self.PLATFORM_NS, self.PLATFORM_NS]
        if self._collection is not None:
            try:
                count = self._collection.count()
                if count > 0:
                    res = self._collection.query(query_texts=[query_text], n_results=min(n_results, count),
                                                 where={"owner_id": {"$in": allowed}})
                    return res.get("documents", [[]])[0]
            except Exception as e:
                logger.warning(f"memory_v01: ChromaDB query failed, falling back ({e})")
        # Fallback: naive substring match over the in-process store — SAME tenancy filter (W343)
        query_lower = query_text.lower()
        matches = [
            f"{v['prompt']}\n{v['response']}"
            for v in self.data.values()
            if v.get("owner_id", self.PLATFORM_NS) in allowed
            and (query_lower in v["prompt"].lower() or query_lower in v["response"].lower())
        ]
        return matches[:n_results]


memory_v01 = MemoryV01()
meeting_log = type('Mock', (), {
    'get_recent_debate': lambda: "No recent debates recorded.",
    'post_argument': lambda *a: None,
    'export_minutes': lambda: "# Minutes",
    'log': []
})()
