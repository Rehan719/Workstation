import logging
import time
from typing import Dict, Any, List, Optional
from agentic_core.db.manager import DatabaseManager

logger = logging.getLogger(__name__)

class PlatformTelemetry:
    """
    ARTICLE 150: Evolutionary Platform Adaptation.
    Collects anonymized usage data to feed the co-evolutionary engine.
    """
    def __init__(self, db: Optional[DatabaseManager] = None):
        self.events = []
        self.db = db

    def log_event(self, persona: str, feature: str, success: bool, metadata: Optional[Dict[str, Any]] = None):
        """
        ARTICLE 150/247: Logs events with spiritual and business KPI context.
        """
        event = {
            "ts": time.time(),
            "persona": persona,
            "feature": feature,
            "success": success,
            "metadata": metadata or {}
        }
        self.events.append(event)
        if self.db:
            # Enhanced logging for dual-metric dashboards
            self.db.log_telemetry(persona, feature, success, metadata)
        logger.info(f"Telemetry: Logged {feature} for {persona} (Success: {success})")

    def get_stats(self) -> Dict[str, Any]:
        return {
            "total_events": len(self.events),
            "success_rate": sum(1 for e in self.events if e["success"]) / max(1, len(self.events))
        }
