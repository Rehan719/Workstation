import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class KnowledgeGraphSeed:
    """
    Tree of All Knowledge - Initial Seed for Biotech.
    Simulates a causal inference graph.
    """
    def __init__(self):
        self.nodes = [
            {"id": "Gene_A", "type": "Protein", "domain": "Biology"},
            {"id": "Compound_X", "type": "Small Molecule", "domain": "Chemistry"},
            {"id": "Pathway_Y", "type": "Metabolic Pathway", "domain": "Biology"},
            {"id": "Effect_Z", "type": "Phenotype", "domain": "Biology"}
        ]
        self.edges = [
            {"source": "Compound_X", "target": "Gene_A", "relation": "BINDS_TO", "confidence": 0.95},
            {"source": "Gene_A", "target": "Pathway_Y", "relation": "PART_OF", "confidence": 0.99},
            {"source": "Pathway_Y", "target": "Effect_Z", "relation": "REGULATES", "confidence": 0.85}
        ]

    def query(self, entity_id: str) -> List[Dict[str, Any]]:
        logger.info(f"TreeOfKnowledge: Querying for entity {entity_id}...")
        return [e for e in self.edges if e["source"] == entity_id or e["target"] == entity_id]

    def add_finding(self, finding: Dict[str, Any]):
        logger.info(f"TreeOfKnowledge: Assimilating new finding: {finding.get('relation')}...")
        self.edges.append(finding)
