import logging

logger = logging.getLogger(__name__)

class DangerSignaling:
    """
    DD-IV, DJ-II: Danger Signal Integration.
    Maps behavioral proxies (dwell time, latency variance) to threat levels.
    Triggered by Article DJ for identity revalidation.
    """
    def map_threat_level(self, dwell_ms: float, latency_var: float) -> str:
        # Dwell time > 750ms is baseline.
        # Excessive dwell (>1500ms) or high variance (>300ms) suggests danger.
        if dwell_ms > 1500 or latency_var > 300:
            level = "CRITICAL_DANGER"
        elif dwell_ms > 1000 or latency_variance > 150:
            level = "MODERATE_THREAT"
        else:
            level = "SAFE"

        logger.info(f"DANGER: Behavior Analysis (Dwell={dwell_ms:.0f}, Var={latency_var:.0f}) -> {level}")
        return level

    def trigger_revalidation(self, level: str) -> bool:
        """Determines if revalidation is required."""
        return level != "SAFE"
