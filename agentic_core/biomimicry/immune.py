import time
import logging
from typing import Dict, Any, List, Optional
import re

class ImmuneOrchestrator:
    """
    Implements Innate and Adaptive Immunity for the Workstation.
    Detects anomalies in the UEG and triggers defensive responses.
    """
    def __init__(self, gaas_validator=None, resilience_manager=None, ueg_callback=None):
        self.logger = logging.getLogger("ImmuneOrchestrator")
        self.gaas = gaas_validator
        self.resilience = resilience_manager
        self.ueg_callback = ueg_callback

        # Adaptive Immunity: Known Anomaly Signatures (Memory B-cells)
        self.anomaly_signatures = [
            r"rapid_request_burst",
            r"unauthorized_genome_access",
            r"metabolic_starvation_loop",
            r"malicious"
        ]

        self.anomaly_scores: Dict[str, float] = {} # entity_id -> score

    def process_event(self, event: Dict[str, Any]):
        """
        Innate Immunity: Scans every UEG event for immediate threats.
        """
        entity_id = event.get("agent_id") or event.get("source", "unknown")
        event_type = event.get("type", "")
        payload_str = str(event.get("payload", ""))

        # Score increment based on suspicious patterns
        score_inc = 0.0
        for pattern in self.anomaly_signatures:
            if re.search(pattern, event_type) or re.search(pattern, payload_str):
                score_inc += 0.3
                self.logger.warning(f"Immune match: Pattern {pattern} detected in event from {entity_id}")

        # Rapid activity check (Innate)
        if event_type == "HIGH_LOAD":
            score_inc += 0.1

        if score_inc > 0:
            current_score = self.anomaly_scores.get(entity_id, 0.0)
            self.anomaly_scores[entity_id] = min(1.0, current_score + score_inc)

            if self.anomaly_scores[entity_id] > 0.95:
                self._trigger_adaptive_response(entity_id, "Critical Anomaly Score")

    def _trigger_adaptive_response(self, entity_id: str, reason: str):
        """
        Adaptive Immunity: Executes complex defense policies.
        (Article 1104 Compliance: Max 60m isolation)
        """
        self.logger.critical(f"IMMUNE RESPONSE: Isolating {entity_id}. Reason: {reason}")

        # 1. Isolate via GaaS (Set Trust Factor to 0)
        if self.gaas:
            self.gaas.trust_factors[entity_id] = 0.0
            self.gaas.set_enforcement_mode("adaptive_immune")

        # 2. Trigger Repair via Resilience Manager
        if self.resilience:
            # Attempt a BER (Base Excision Repair) or Apoptosis
            self.logger.info(f"Immune: Handing off {entity_id} to Resilience Manager.")
            # In Phase 2, we simulate the handoff

        self._emit_event("IMMUNE_ISOLATION", {
            "entity_id": entity_id,
            "reason": reason,
            "duration_limit": "60m"
        })

    def _emit_event(self, event_type: str, data: Dict[str, Any]):
        event = {
            "source": "ImmuneOrchestrator",
            "type": event_type,
            "payload": data,
            "timestamp": time.time()
        }
        if self.ueg_callback:
            self.ueg_callback(event)

if __name__ == "__main__":
    def autonomous_ueg(e): print(f"UEG -> {e['type']} ({e['payload'].get('entity_id', '')})")
    immune = ImmuneOrchestrator(ueg_callback=autonomous_ueg)

    # Simulate a series of suspicious events
    for _ in range(4):
        immune.process_event({
            "source": "agent_x",
            "type": "unauthorized_genome_access_attempt",
            "payload": {"target": "Article_1"}
        })
