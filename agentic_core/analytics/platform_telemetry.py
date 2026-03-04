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

    def log_event(self, persona: str, feature: str, success: bool):
        event = {
            "ts": time.time(),
            "persona": persona,
            "feature": feature,
            "success": success
        }
        self.events.append(event)
        if self.db:
            self.db.log_telemetry(persona, feature, success)
        logger.info(f"Telemetry: Logged {feature} for {persona}")

    def get_stats(self) -> Dict[str, Any]:
        return {
            "total_events": len(self.events),
            "success_rate": sum(1 for e in self.events if e["success"]) / max(1, len(self.events))
        }
