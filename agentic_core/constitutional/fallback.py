from typing import Dict, Any, List
from .ueg_logger import UEGLogger

class FallbackProtocol:
    """
    Tiered fallback protocol (Levels 1-4).
    """
    def __init__(self, domain: str):
        self.domain = domain
        self.logger = UEGLogger()
        self.violation_count = 0

    def trigger(self, level: int, reason: str, details: Dict[str, Any] = None):
        """
        Triggers a specific fallback level.
        """
        if level > 1: # Only count critical levels towards suspension
            self.violation_count += 1

        # Check for immediate escalation to level 4
        effective_level = level
        if self.violation_count >= 10:
            effective_level = 4

        self.logger.log_event(self.domain, f"FALLBACK_LEVEL_{effective_level}", {
            "reason": reason,
            "details": details,
            "violation_count": self.violation_count
        })

        if effective_level == 1:
            return self._level_1_warning(reason)
        elif effective_level == 2:
            return self._level_2_reduced_automation(reason)
        elif effective_level == 3:
            return self._level_3_manual_review(reason)
        elif effective_level == 4:
            return self._level_4_suspension(reason)

    def _level_1_warning(self, reason: str):
        print(f"[FALLBACK L1] Warning in {self.domain}: {reason}")
        return {"action": "CONTINUE", "status": "warning"}

    def _level_2_reduced_automation(self, reason: str):
        print(f"[FALLBACK L2] Reduced automation in {self.domain}: {reason}")
        return {"action": "PLACEHOLDER", "status": "degraded"}

    def _level_3_manual_review(self, reason: str):
        print(f"[FALLBACK L3] MANUAL REVIEW REQUIRED in {self.domain}: {reason}")
        # In Q2, we watermark the output as UNVERIFIED
        return {"action": "WATERMARK_UNVERIFIED", "status": "blocked"}

    def _level_4_suspension(self, reason: str):
        print(f"[FALLBACK L4] DOMAIN SUSPENDED: {self.domain}. Reason: {reason}")
        return {"action": "HALT", "status": "suspended"}

    def evaluate_violations(self, violations: List[Dict[str, Any]]):
        """
        Evaluates violations and determines fallback level.
        """
        if not violations:
            # Still check if we reached suspension from previous events
            if self.violation_count >= 10:
                return self.trigger(4, "Threshold for total violations exceeded.")
            return None

        if self.violation_count >= 10:
            return self.trigger(4, "Threshold for total violations exceeded.")

        reject_count = sum(1 for v in violations if v["status"] == "reject")

        if reject_count >= 3:
            return self.trigger(3, "Multiple critical violations in single package.")
        elif reject_count >= 1:
            return self.trigger(2, "Critical violation detected.")
        else:
            return self.trigger(1, "Non-critical violation detected.")
