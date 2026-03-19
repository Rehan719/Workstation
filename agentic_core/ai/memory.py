from typing import List, Dict, Any
import json
import os

class VectorMemory:
    """v148.0 Lightweight Vector Memory (JSON-based for POC)."""
    def __init__(self):
        self.storage_path = "agentic_core/data/memory.json"
        self._init_storage()

    def _init_storage(self):
        if not os.path.exists(self.storage_path):
            with open(self.storage_path, "w") as f:
                json.dump([], f)

    def add_memory(self, text: str, metadata: Dict[str, Any] = {}):
        with open(self.storage_path, "r") as f:
            memories = json.load(f)
        memories.append({"text": text, "metadata": metadata})
        with open(self.storage_path, "w") as f:
            json.dump(memories, f)

    def query_memory(self, query: str) -> List[str]:
        """Simple keyword matching for POC RAG."""
        with open(self.storage_path, "r") as f:
            memories = json.load(f)
        results = [m["text"] for m in memories if query.lower() in m["text"].lower()]
        return results[:5]

memory = VectorMemory()
