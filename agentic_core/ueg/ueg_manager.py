import json
import os
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class UEGManager:
    """
    v60 Mastery: Unified Evidence Graph Manager.
    Manages the semantic relationships and provenance of all scientific claims.
    """
    def __init__(self, storage_path: str = "meta/ueg_graph.json"):
        self.storage_path = storage_path
        self.graph = self._load_graph()

    def _load_graph(self) -> Dict[str, Any]:
        if os.path.exists(self.storage_path):
            with open(self.storage_path, 'r') as f:
                return json.load(f)
        return {"nodes": [], "edges": []}

    def add_claim(self, claim: str, evidence: List[str], claim_type: str = "hypothesis"):
        node = {
            "id": f"claim_{len(self.graph['nodes'])}",
            "type": claim_type,
            "content": claim,
            "evidence": evidence
        }
        self.graph["nodes"].append(node)
        self._save()
        return node

    def _save(self):
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
        with open(self.storage_path, 'w') as f:
            json.dump(self.graph, f, indent=4)
