import logging
from typing import List, Dict, Any
from core.models import AnalysisDossier, ProposalPackage
from core.provenance_graph import ProvenanceGraph

logger = logging.getLogger(__name__)

class MuainaEngine:
    def __init__(self, domain_config: Dict[str, Any], provenance: ProvenanceGraph):
        self.config = domain_config
        self.provenance = provenance
        self.muaina_config = self.config.get("muaina", {})

    def develop_proposal(self, dossier: AnalysisDossier, option_id: str) -> ProposalPackage:
        templates = self.muaina_config.get("output_templates", [])
        package = ProposalPackage(
            analysis_ref=dossier.evidence_graph_ref,
            title=f"Proposal for {option_id}",
            description=f"Action plan generated using {templates[0] if templates else 'default'} template",
            roadmap=[{"phase": "1", "action": "Implement monitoring"}],
            success_metrics={"precision": 0.95},
            verification_protocol={"type": "empirical"}
        )
        self.provenance.add_node("proposal", package.model_dump_json(), parents=[dossier.evidence_graph_ref])
        return package
