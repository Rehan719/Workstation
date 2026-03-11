import json
import os
import logging
from typing import Dict, Any
import os
import logging
from typing import Dict, Any, List
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class EvolutionaryMemory:
    """CN-V: Evolutionary Memory Storage in the UEG."""

    def __init__(self, storage_path: str = "meta/ueg_graph.json"):
        self.storage_path = storage_path

    def store_synthesis_results(self, result: Dict[str, Any]):
        """Persists the grand synthesis results."""
        try:
            with open(self.storage_path, "w") as f:
                json.dump(result, f, indent=4)
            logger.info(f"Synthesis results stored in {self.storage_path}")
        except Exception as e:
            logger.error(f"Failed to store memory: {e}")
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

        version = results.get("version", "unknown")
        import datetime
        timestamp = datetime.datetime.now().isoformat()

        ueg["nodes"].append({
            "id": f"synthesis_{version}_{timestamp}",
            "type": "insight",
            "content": results,
            "metadata": {"version": version, "timestamp": timestamp}
        })

    def store_external_knowledge(self, insights: List[Dict[str, Any]]):
        """Stores extracted insights from LLM conversations (Article 357)."""
        logger.info(f"Storing {len(insights)} external insights in UEG.")

        # Load existing
        ueg = {"nodes": []}
        if os.path.exists(self.ueg_path):
            try:
                with open(self.ueg_path, "r") as f:
                    ueg = json.load(f)
            except Exception: pass

        for i, insight in enumerate(insights):
            ueg["nodes"].append({
                "id": f"external_insight_{i}_{insight['theme']}",
                "type": "LLMConversation",
                "content": insight,
                "metadata": {"source": insight["source"], "quality": insight["quality_score"]}
            })

        with open(self.ueg_path, "w") as f:
            json.dump(ueg, f, indent=4)
