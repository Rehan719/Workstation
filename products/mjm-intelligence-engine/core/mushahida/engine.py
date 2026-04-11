import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
from core.models import EvidenceGraph, EvidenceItem, EvidenceSource
from core.provenance_graph import ProvenanceGraph

logger = logging.getLogger(__name__)

class MushahidaEngine:
    def __init__(self, domain_config: Dict[str, Any], provenance: ProvenanceGraph):
        self.config = domain_config
        self.provenance = provenance
        self.mush_config = self.config.get("mushahida", {})

    def acquire_evidence(self, queries: List[str]) -> EvidenceGraph:
        logger.info(f"Acquiring evidence for {self.config.get('domain', {}).get('id')}")
        graph = EvidenceGraph()
        allowed_sources = self.mush_config.get("allowed_sources", [])

        for query in queries:
            content = f"Simulated evidence for: {query}"
            source = EvidenceSource(
                type=allowed_sources[0] if allowed_sources else "web_search",
                uri="https://example.com/source",
                timestamp=datetime.utcnow()
            )
            item = EvidenceItem.create(content, source)
            node_id = self.provenance.add_node("evidence", content, metadata={"query": query})
            item.tags = [node_id] # Use tags as proxy for causal links in pydantic model
            graph.items.append(item)
        return graph
