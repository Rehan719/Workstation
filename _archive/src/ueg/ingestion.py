from typing import Any, Dict, Optional
from .ledger import UnifiedEvidenceGraph

class IngestionHooks:
    """
    Automated ingestion of system artifacts into the UEG.
    """
    def __init__(self, ueg: UnifiedEvidenceGraph):
        self.ueg = ueg

    def ingest_artifact(self, artifact_id: str, artifact_type: str, metadata: Dict[str, Any], source: str):
        """Creates a node and links it to its source."""
        self.ueg.add_node(artifact_id, artifact_type, metadata)
        if source:
            self.ueg.add_edge(source, artifact_id, 'PRODUCED_ARTIFACT')

    def ingest_dataset(self, dataset_id: str, metadata: Dict[str, Any]):
        self.ueg.add_node(dataset_id, 'DATASET', metadata)

    def ingest_hypothesis(self, hypothesis_id: str, metadata: Dict[str, Any], evidence_links: list):
        self.ueg.add_node(hypothesis_id, 'HYPOTHESIS', metadata)
        for evidence in evidence_links:
            self.ueg.add_edge(evidence, hypothesis_id, 'SUPPORTS')
