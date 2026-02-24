import logging
import time
import hashlib
from typing import Dict, Any, List
from agentic_core.pulse.pulse_clock import PulseClock

logger = logging.getLogger(__name__)

class SurvivalEngineV2:
    """
    BT: Survival Instinct Engine v2.0.
    Supreme meta-governor with hard real-time veto mechanics and strict hierarchy.
    """
    def __init__(self, clock: PulseClock):
        self.clock = clock
        self.priority_hierarchy = ["immune", "nervous", "digestive", "aging"]
        self.veto_history = []
        self.sigma_threshold = 0.87 # BT-III

    def request_action(self, system: str, action: Dict[str, Any]) -> bool:
        """Gates actions based on priority and real-time safety thresholds."""
        start_pulse = self.clock.get_current_pulse()

        # 1. Hierarchy Check
        if not self._verify_hierarchy(system, action):
            self.trigger_veto(system, "Hierarchy Violation")
            return False

        # 2. Threshold Monitor
        deviation = action.get("deviation", 0.0)
        if deviation > self.sigma_threshold:
            self.trigger_veto(system, f"Threshold Breach ({deviation:.2f}σ)")
            return False

        return True

    def trigger_veto(self, source: str, reason: str):
        """BT-II: Real-Time Veto Interface."""
        pulse = self.clock.get_current_pulse()
        # BT-IV: Cryptographic Authentication (Simulated)
        auth_tag = hashlib.sha256(f"VETO:{pulse}:{reason}".encode()).hexdigest()[:8]

        entry = {
            "pulse": pulse,
            "source": source,
            "reason": reason,
            "auth_tag": f"sig:{auth_tag}",
            "timestamp": time.time()
        }
        self.veto_history.append(entry)
        logger.error(f"HARD REAL-TIME VETO: [{source}] {reason} @ Pulse {pulse}")
        return entry

    def _verify_hierarchy(self, system: str, action: Dict[str, Any]) -> bool:
        target = action.get("target_subsystem")
        if not target: return True

        try:
            source_rank = self.priority_hierarchy.index(system.lower())
            target_rank = self.priority_hierarchy.index(target.lower())
            return source_rank <= target_rank
        except ValueError:
            return True
