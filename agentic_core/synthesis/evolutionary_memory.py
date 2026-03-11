import json
import os
import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class EvolutionaryMemory:
    """CN-V: Evolutionary Memory Storage in the UEG."""

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

        # Ensure ueg is a dict and has nodes
        if not isinstance(ueg, dict):
            ueg = {"nodes": []}
        if "nodes" not in ueg:
            ueg["nodes"] = []

        node_id = f"v{results.get('version', '100.0.0')}_grand_synthesis"

        # Avoid duplicates
        ueg["nodes"] = [n for n in ueg["nodes"] if n.get("id") != node_id]

        # Add synthesis insight node
        ueg["nodes"].append({
            "id": node_id,
            "type": "insight",
            "content": results,
            "metadata": {"version": results.get('version', '100.0.0'), "timestamp": "2024-10-01T00:00:00"}
        })

        os.makedirs(os.path.dirname(self.ueg_path), exist_ok=True)
        with open(self.ueg_path, "w") as f:
            json.dump(ueg, f, indent=4)
