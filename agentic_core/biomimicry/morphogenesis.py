import time
import logging
from typing import Dict, Any

class MorphogenesisOrchestrator:
    """
    Dynamically adjusts service mesh topology based on load.
    Triggers agent spawning or migration.
    """
    def __init__(self, ueg_callback=None):
        self.logger = logging.getLogger("MorphogenesisOrchestrator")
        self.ueg_callback = ueg_callback
        self.topology = {"nodes": ["core_node_1"], "connections": []}

    def adapt_topology(self, demand_signal: str):
        """
        Grows or prunes the system structure.
        """
        action = "IDLE"
        if demand_signal == "HIGH_LOAD":
            new_node = f"worker_node_{len(self.topology['nodes'])}"
            self.topology["nodes"].append(new_node)
            self.topology["connections"].append(("core_node_1", new_node))
            action = "NODE_SPAWN"
        elif demand_signal == "LOW_LOAD" and len(self.topology["nodes"]) > 1:
            removed = self.topology["nodes"].pop()
            # Prune connections (simplified)
            self.topology["connections"] = [c for c in self.topology["connections"] if removed not in c]
            action = "NODE_PRUNE"

        if action != "IDLE":
            self._emit_event("MORPHOGENIC_SHIFT", {
                "action": action,
                "current_nodes": len(self.topology["nodes"])
            })
            self.logger.info(f"Morphogenesis: {action} triggered. Nodes: {len(self.topology['nodes'])}")

    def _emit_event(self, event_type: str, data: Dict[str, Any]):
        event = {
            "source": "MorphogenesisOrchestrator",
            "type": event_type,
            "payload": data,
            "timestamp": time.time()
        }
        if self.ueg_callback:
            self.ueg_callback(event)

if __name__ == "__main__":
    def autonomous_ueg(e): print(f"UEG -> {e['type']} ({e['payload']['action']})")
    mo = MorphogenesisOrchestrator(autonomous_ueg)
    mo.adapt_topology("HIGH_LOAD")
    mo.adapt_topology("LOW_LOAD")
