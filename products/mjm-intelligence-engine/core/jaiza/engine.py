import logging
from typing import List, Dict, Any
from core.models import EvidenceGraph, AnalysisDossier
from core.provenance_graph import ProvenanceGraph

logger = logging.getLogger(__name__)

class JaizaEngine:
    def __init__(self, domain_config: Dict[str, Any], provenance: ProvenanceGraph):
        self.config = domain_config
        self.provenance = provenance
        self.jaiza_config = self.config.get("jaiza", {})

    def analyze(self, graph: EvidenceGraph) -> AnalysisDossier:
        patterns = self.jaiza_config.get("pattern_libraries", [])
        dossier = AnalysisDossier(
            evidence_graph_ref=str(graph.created_at.timestamp()),
            patterns=[{"id": p, "type": "matched"} for p in patterns],
            risks=[{"type": "procedural_gap", "severity": "high"}],
            strategic_options=[{"id": "opt-1", "description": "Regulatory realignment"}],
            confidence_intervals={"overall": 0.88}
        )
        parent_ids = []
        for item in graph.items:
            parent_ids.extend(item.tags)
        self.provenance.add_node("analysis", dossier.model_dump_json(), parents=parent_ids)
        return dossier
