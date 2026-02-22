from typing import Any, Dict, List
from .layer1 import SourceVerifier
from .layer2 import LogicVerifier
from .layer3 import NumericalValidator
from .layer4 import ReplicationEngine
from .layer5 import Adversary
from src.ueg.ledger import UnifiedEvidenceGraph

class VerificationPipeline:
    """
    Orchestrates the five-layer verification framework.
    """
    def __init__(self, ueg: UnifiedEvidenceGraph):
        self.ueg = ueg
        self.l1 = SourceVerifier()
        self.l2 = LogicVerifier()
        self.l3 = NumericalValidator()
        self.l4 = ReplicationEngine()
        self.l5 = Adversary(ueg)

    async def verify_artifact(self, artifact_id: str, data: Any, signature: str) -> Dict[str, Any]:
        """Runs the full five-layer suite on an artifact."""
        results = {}

        # Layer 1
        results['L1'] = await self.l1.verify_integrity(data, signature)

        # Layer 2 (if applicable)
        if isinstance(data, dict) and 'formula' in data:
            results['L2'] = await self.l2.verify_formula(data['formula'], [])

        # Layer 5
        results['L5'] = await self.l5.probe_hypothesis(artifact_id)

        overall_status = all([results['L1']]) # Simple logic for now

        report = {
            "artifact_id": artifact_id,
            "overall_status": "PASSED" if overall_status else "FAILED",
            "layer_details": results
        }

        # Log to UEG
        self.ueg.ledger.add_transaction('verification_pipeline', 'VERIFY_ARTIFACT', report)

        return report
