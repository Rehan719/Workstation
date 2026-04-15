import logging
import time
from typing import Dict, Any, List, Optional
from .ueg_logger import UEGLogger

class MJMLearningEngine:
    """
    ARTICLE 10.1: MJM Learning Engine (Cognitive Cortex).
    Handles feedback loops, pattern extraction, and governed evolution.
    """
    def __init__(self, domain_config: Dict[str, Any], ueg: UEGLogger):
        self.config = domain_config
        self.ueg = ueg
        self.learning_signals = []
        self.evolution_triggers = domain_config.get("learning_engine", {}).get("evolution_triggers", {})
        self.logger = logging.getLogger("LearningEngine")

    def ingest_feedback(self, feedback_data: Dict[str, Any]):
        """Ingests feedback from Mushahida, Jaiza, or Muaina phases."""
        signal = {
            "timestamp": time.time(),
            "data": feedback_data,
            "type": feedback_data.get("type", "generic_feedback")
        }
        self.learning_signals.append(signal)

        self.ueg.log_constitutional_event({
            "type": "learning_signal_ingested",
            "signal_type": signal["type"]
        })

        if self._should_trigger_evolution():
            self._trigger_evolution()

    def _should_trigger_evolution(self) -> bool:
        """Determines if enough signals exist to trigger an evolution event."""
        threshold = self.evolution_triggers.get("evidence_volume_threshold", 50)
        print(f"DEBUG: Learning signals: {len(self.learning_signals)}, Threshold: {threshold}")
        return len(self.learning_signals) >= threshold

    def _trigger_evolution(self):
        """Proposes a constitutional rule weight update or pattern refinement."""
        self.logger.info("TRIGGERING CONSTITUTIONAL EVOLUTION...")

        evolution_proposal = {
            "type": "rule_weight_evolution",
            "reason": f"Accumulated {len(self.learning_signals)} learning signals.",
            "proposed_changes": {"regulatory_compliance_weight": 0.22},
            "evidence_hash": self.ueg.log_constitutional_event({"type": "evolution_proposal_generated"})
        }

        # Clear signals after proposal
        self.learning_signals = []
        return evolution_proposal

    def get_cognitive_report(self) -> Dict[str, Any]:
        return {
            "signal_count": len(self.learning_signals),
            "evolution_triggers": self.evolution_triggers,
            "status": "active_learning"
        }
