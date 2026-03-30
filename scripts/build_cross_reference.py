import os
import json
import hashlib
from typing import Dict, Any, List
from datetime import datetime

class CrossReferenceIndex:
    """
    Master citation log mapping factual assertions to source metadata,
    pipeline identifiers, and Entity signatures.
    """
    def __init__(self, storage_path: str = "data/organism/cross_reference_index.json"):
        self.storage_path = storage_path
        self.index: List[Dict[str, Any]] = []

    def log_assertion(self, assertion: str, source: str, page: int, para: int, pipeline: str, signature: str, audit_hash: str):
        entry = {
            "assertion": assertion,
            "source_metadata": {
                "file": source,
                "page": page,
                "paragraph": para
            },
            "pipeline_id": pipeline,
            "entity_signature": signature,
            "audit_hash": audit_hash,
            "timestamp": datetime.utcnow().isoformat()
        }
        self.index.append(entry)
        self._save()

    def _save(self):
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
        with open(self.storage_path, "w") as f:
            json.dump(self.index, f, indent=2)

if __name__ == "__main__":
    idx = CrossReferenceIndex()
    # Demo entries for Exhibit Q-1 and Disability Disclosure
    idx.log_assertion(
        "Exhibit Q-1: 94% punctuality record maintained despite lack of adjustments.",
        "inputs/Minhas_Contemporaneous_Log_6Oct20252.pdf",
        5, 2, "ingestion_pipeline_v1.0", "RSA-2048-SIG-Q1", "sha256:d3e2..."
    )
    print("Cross-Reference Index initialized with key forensic anchors.")
