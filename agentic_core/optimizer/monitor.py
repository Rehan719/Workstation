import logging
import psutil
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class ResourceMonitor:
    """
    ARTICLE 311: Resource Monitor.
    Tracks real-time system telemetry.
    """
    def __init__(self):
        self.history: List[Dict[str, Any]] = []

    def get_current_usage(self) -> Dict[str, Any]:
        """Captures real-time metrics including process-level telemetry."""
        #  W746 - the one host observation. memory_mb is THIS PROCESS's resident memory and the two percentages
        #  are the HOST's; they sat side by side unnamed, and now each says which it is.
        from agentic_core.organism.host_observation import observe as _observe_host
        _obs = _observe_host()
        usage = {
            "timestamp": psutil.time.time(),
            "cpu_percent": _obs["host"]["cpu_percent"],
            "memory_mb": _obs["process"]["rss_mb"],
            "memory_mb_scope": "process",
            "memory_percent": _obs["host"]["memory_percent"],
            "percent_scope": "host",
            "disk_usage": psutil.disk_usage('/').percent,
            "api_quota_remaining": 0.85 # Simulation baseline
        }
        self.history.append(usage)
        # Keep only last 1000 records
        if len(self.history) > 1000:
            self.history.pop(0)

        logger.debug(f"Monitor: Usage: {usage}")
        return usage

    def get_history(self, limit: int = 100) -> List[Dict[str, Any]]:
        return self.history[-limit:]
