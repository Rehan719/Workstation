import json
import os
import logging
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)

class OntologyEngine:
    """ARTICLE 60: Domain Truth Validation & Ontology Querying."""
    def __init__(self, data_path: str = "agentic_core/data/ontologies"):
        # W473 (refutation) — a reader: importing it no longer creates the directory it reads (an empty directory
        # under the repository said "ontologies" where there are none; nothing here ever writes one)
        self.data_path = data_path
        self.cache: Dict[str, Any] = {}

    # W506 (FU-077) - AN ABSENCE IS NOT AN EMPTY GRAPH. This returned {"nodes": [], "links": []} for every
    # domain, which a caller reads as "the ontology was consulted and held nothing". No ontology is
    # installed at the path this engine reads, and that is a different statement.
    #
    # Real ontologies DO exist elsewhere in the tree (knowledge/Law/EmploymentTribunal/ontology/,
    # knowledge/Employment/ontology/, knowledge/Religion/ontology/) and none of them uses this engine's
    # `nodes` schema - the three have three different shapes. Wiring them is a schema mapping, and for the
    # law domain it waits on the Owner (FU-272), so it is a separate task rather than a path change here.
    UNAVAILABLE_BASIS = ("no ontology file is installed at the path this engine reads. Ontologies exist "
                         "elsewhere in the repository under knowledge/, in schemas this engine does not "
                         "read; mapping them is not done. This is an absence, not an empty ontology.")

    def get_ontology(self, domain: str) -> Dict[str, Any]:
        if domain in self.cache:
            return self.cache[domain]

        path = os.path.join(self.data_path, f"{domain}.json")
        try:
            if not os.path.exists(path):
                return {"available": False, "domain": domain, "path_read": path,
                        "basis": self.UNAVAILABLE_BASIS, "nodes": [], "links": []}
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            data.setdefault("available", True)
            self.cache[domain] = data
            return data
        except (FileNotFoundError, json.JSONDecodeError) as exc:
            logger.error("OntologyEngine: %s ontology could not be read (%s)", domain, exc)
            return {"available": False, "domain": domain, "path_read": path,
                    "basis": f"the ontology file exists and could not be read: {exc}",
                    "nodes": [], "links": []}

    def searched(self, domain: str, query: str) -> Dict[str, Any]:
        """W506 (FU-077) - the results AND whether an ontology was consulted at all.

        `search_ontology` returns a bare list, and a caller cannot tell "no matches in a real ontology"
        from "there is no ontology". The weaver read the bare list and asserted cross-domain findings over
        it, so the distinction has to be available to callers.
        """
        ontology = self.get_ontology(domain)
        return {"domain": domain, "query": query,
                "available": bool(ontology.get("available")),
                "basis": ontology.get("basis"),
                "results": self.search_ontology(domain, query)}

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
