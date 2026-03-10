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
        process = psutil.Process()
        usage = {
            "timestamp": psutil.time.time(),
            "cpu_percent": psutil.cpu_percent(),
            "memory_mb": process.memory_info().rss / (1024 * 1024),
            "memory_percent": psutil.virtual_memory().percent,
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
