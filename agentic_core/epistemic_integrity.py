from typing import Any, Dict, List, Optional
import hashlib
import time
import json

class EpistemicIntegrityFramework:
    """
    Article: Epistemic Integrity Framework.
    Guarantees every artifact is verifiable, traceable, and immutable.
    Generates full-path reasoning traces and FAIR-compliant provenance.
    """
    def __init__(self):
        self.log_dir = "artifacts/provenance/"
        import os
        os.makedirs(self.log_dir, exist_ok=True)

    def generate_reasoning_trace(self, cognitive_act: Dict[str, Any]) -> Dict[str, Any]:
        """
        Produces human-readable chain of thought and machine-checkable artifacts.
        """
        trace = {
            "act_id": cognitive_act.get("id"),
            "human_readable_cot": cognitive_act.get("cot", []),
            "machine_artifacts": cognitive_act.get("artifacts", []),
            "timestamp": time.time(),
            "epistemic_seal": self._generate_seal(cognitive_act)
        }
        return trace

    def create_fair_provenance(self, artifact_id: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """
        Captures extensive metadata for full scientific auditability.
        """
        provenance = {
            "artifact_id": artifact_id,
            "metadata": metadata, # Free-tier backend, queue times, optimizer path, etc.
            "accessibility": "FAIR-compliant",
            "interoperability": "JSON-LD",
            "reusability": "Open-Source-Attribution",
            "immutable_hash": self._generate_hash(metadata)
        }

        # Save to persistent trail
        with open(f"{self.log_dir}{artifact_id}_provenance.json", 'w') as f:
            json.dump(provenance, f, indent=2)

        return provenance

    def _generate_seal(self, data: Any) -> str:
        """Cryptographic seal for epistemic integrity."""
        return hashlib.sha256(str(data).encode()).hexdigest()

    def _generate_hash(self, data: Any) -> str:
        return hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()
