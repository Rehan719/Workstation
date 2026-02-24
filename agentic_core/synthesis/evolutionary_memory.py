import json
import os
import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class EvolutionaryMemory:
    """Stores synthesis results and insights in the Unified Evidence Graph (UEG)."""

    def __init__(self, ueg_path: str = "meta/ueg_graph.json"):
        self.ueg_path = ueg_path

    def load_previous_insights(self) -> List[Dict[str, Any]]:
        if os.path.exists(self.ueg_path):
            try:
                with open(self.ueg_path, "r") as f:
                    ueg = json.load(f)
                    return [n for n in ueg.get("nodes", []) if n.get("type") == "insight"]
            except Exception:
                return []
        return []

    def store_synthesis_results(self, results: Dict[str, Any]):
        logger.info(f"Storing synthesis results in UEG at {self.ueg_path}")

        # Load existing UEG or create new
        ueg = {}
        if os.path.exists(self.ueg_path):
            try:
                with open(self.ueg_path, "r") as f:
                    ueg = json.load(f)
            except Exception:
                ueg = {}

        # Add synthesis insight node
        if "nodes" not in ueg: ueg["nodes"] = []

        ueg["nodes"].append({
            "id": "v60_grand_synthesis",
            "type": "insight",
            "content": results,
            "metadata": {"version": "60.0.0", "timestamp": "2024-05-22T10:00:00"}
        })

        with open(self.ueg_path, "w") as f:
            json.dump(ueg, f, indent=4)
