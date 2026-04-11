from typing import Dict, Any, List
import hashlib
from ..omnimedia.decision_engine_v4 import OmnimediaDecisionEngineV4

class ImmuneLearner:
    def __init__(self, decision_engine: OmnimediaDecisionEngineV4, logger: Any):
        self.decision_engine = decision_engine
        self.logger = logger

    def compute_signature(self, failure_type: str, context: Dict[str, Any]) -> str:
        sig_base = f"{failure_type}_{context.get('format')}_{context.get('pipeline')}_{context.get('mode')}"
        return hashlib.sha256(sig_base.encode()).hexdigest()

    def learn_from_failure(self, failure_type: str, context: Dict[str, Any]):
        signature = self.compute_signature(failure_type, context)
        self.decision_engine.record_failure(signature, failure_type)

        count = self.decision_engine.get_failure_count(signature)
        if count >= 3:
            self.logger.log_event({
                "operation": "IMMUNE_ALERT",
                "signature": signature,
                "failure_type": failure_type,
                "message": "Repeated failure detected. Triggering proactive fallback."
            })
            return True # Trigger proactive fallback
        return False

    def is_pathogen_present(self, context: Dict[str, Any]) -> bool:
        # Pre-check if a known failure pattern exists for this context
        # Simplified: we check a generic 'any_failure' type for this context
        signature = self.compute_signature("general_failure", context)
        return self.decision_engine.get_failure_count(signature) >= 3
