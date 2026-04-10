import time
import logging
from typing import Dict, Any, List, Optional

class EmergentBehaviourAnalyser:
    """
    Analyzes UEG events for emergent patterns: leadership, specialisation, altruism.
    Feeds insights back into the fitness function for swarm selection.
    """
    def __init__(self, ueg_callback=None):
        self.logger = logging.getLogger("EmergenceAnalyser")
        self.ueg_callback = ueg_callback
        # pattern_counters: agent_id -> pattern -> count
        self.pattern_stats: Dict[str, Dict[str, int]] = {}

    def ingest_event(self, event: Dict[str, Any]):
        """
        Scans an event for behavioral markers.
        """
        agent_id = event.get("source")
        if not agent_id: return

        if agent_id not in self.pattern_stats:
            self.pattern_stats[agent_id] = {"specialisation": 0, "leadership": 0, "altruism": 0}

        event_type = event.get("type", "")

        # 1. Leadership: agent coordinates others (e.g., SWARM_FORMED leader)
        if event_type == "SWARM_FORMED" and event["payload"].get("leader") == agent_id:
            self.pattern_stats[agent_id]["leadership"] += 1

        # 2. Altruism: agent shares resource with others (Symbiosis exchange)
        if event_type == "RESOURCE_EXCHANGE" and event["payload"].get("provider") == agent_id:
            self.pattern_stats[agent_id]["altruism"] += 1

        # 3. Specialisation: high frequency of specific task types
        if event_type == "TASK_ALLOCATED":
            self.pattern_stats[agent_id]["specialisation"] += 1

        # Periodic assessment
        if sum(self.pattern_stats[agent_id].values()) % 10 == 0:
            self._report_emergence(agent_id)

    def _report_emergence(self, agent_id: str):
        stats = self.pattern_stats[agent_id]
        self.logger.info(f"Emergence detected for {agent_id}: {stats}")
        self._emit_event("EMERGENT_INSIGHT", {
            "agent_id": agent_id,
            "patterns": stats,
            "synergy_multiplier": 1.0 + (stats["altruism"] * 0.05)
        })

    def _emit_event(self, event_type: str, data: Dict[str, Any]):
        event = {
            "source": "EmergenceAnalyser",
            "type": event_type,
            "payload": data,
            "timestamp": time.time()
        }
        if self.ueg_callback:
            self.ueg_callback(event)

if __name__ == "__main__":
    def mock_ueg(e): print(f"UEG -> {e['type']} ({e['payload'].get('agent_id', '')})")
    analyser = EmergentBehaviourAnalyser(mock_ueg)

    # Simulate events
    for _ in range(10):
        analyser.ingest_event({"source": "agent_alpha", "type": "TASK_ALLOCATED", "payload": {}})

    analyser.ingest_event({
        "source": "agent_beta",
        "type": "RESOURCE_EXCHANGE",
        "payload": {"provider": "agent_beta"}
    })
