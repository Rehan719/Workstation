import json
import os
import logging
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)

class OntologyEngine:
    """ARTICLE 60: Domain Truth Validation & Ontology Querying."""
    def __init__(self, data_path: str = "agentic_core/data/ontologies"):
        if not os.path.exists(data_path):
             os.makedirs(data_path, exist_ok=True)
        self.data_path = data_path
        self.cache: Dict[str, Any] = {}

    def get_ontology(self, domain: str) -> Dict[str, Any]:
        if domain in self.cache:
            return self.cache[domain]

        path = os.path.join(self.data_path, f"{domain}.json")
        try:
            if not os.path.exists(path):
                 return {"nodes": [], "links": []}
            with open(path, "r") as f:
                data = json.load(f)
                self.cache[domain] = data
                return data
        except (FileNotFoundError, json.JSONDecodeError):
            logger.error(f"OntologyEngine: {domain} ontology not found.")
            return {"nodes": [], "links": []}

    def search_ontology(self, domain: str, query: str) -> List[Dict[str, Any]]:
        ontology = self.get_ontology(domain)
        nodes = ontology.get("nodes", [])
        results = []
        for node in nodes:
            node_id = node.get("id", str(node)) if isinstance(node, dict) else str(node)
            if query.lower() in node_id.lower():
                results.append(node if isinstance(node, dict) else {"id": node})
        return results

ontology_engine = OntologyEngine()
