import hashlib
import json
from datetime import datetime
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

class ProvenanceNode(BaseModel):
    id: str
    type: str # evidence, analysis, proposal
    content_hash: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    causal_parents: List[str] = Field(default_factory=list)

class ProvenanceGraph:
    """
    Immutable memory with causal tracing for the MJM Engine.
    Handles the linking of evidence to analysis and proposals.
    """
    def __init__(self):
        self.nodes: Dict[str, ProvenanceNode] = {}

    def add_node(self, node_type: str, content: str, parents: List[str] = None, metadata: Dict[str, Any] = None) -> str:
        content_hash = hashlib.sha256(content.encode()).hexdigest()
        node_id = f"{node_type[:3].upper()}-{content_hash[:8]}-{int(datetime.utcnow().timestamp())}"

        node = ProvenanceNode(
            id=node_id,
            type=node_type,
            content_hash=content_hash,
            causal_parents=parents or [],
            metadata=metadata or {}
        )
        self.nodes[node_id] = node
        return node_id

    def get_lineage(self, node_id: str) -> List[ProvenanceNode]:
        """Traces back all causal parents for a given node."""
        lineage = []
        queue = [node_id]
        visited = set()

        while queue:
            current_id = queue.pop(0)
            if current_id in visited or current_id not in self.nodes:
                continue

            node = self.nodes[current_id]
            lineage.append(node)
            visited.add(current_id)
            queue.extend(node.causal_parents)

        return lineage

    def export_json_ld(self) -> str:
        """Exports the graph in JSON-LD format for interoperability."""
        return json.dumps({
            "@context": "https://workstation.local/provenance",
            "nodes": [node.model_dump() for node in self.nodes.values()]
        }, indent=2, default=str)
