import logging
import json
import os
from typing import Dict, Any, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class CollectiveMemory:
    """
    ARTICLE 316: Collective Intelligence & Memory.
    Propagates successful strategies via a structured knowledge graph.
    Maintains temporal context for evolutionary learning.
    """
    def __init__(self, storage_path: str = "meta/collective_memory.json"):
        self.storage_path = storage_path
        self.memory_store: List[Dict[str, Any]] = self._load_memory()

    def _load_memory(self) -> List[Dict[str, Any]]:
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Memory: Failed to load: {e}")
        return []

    def _save_memory(self):
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
        try:
            with open(self.storage_path, 'w') as f:
                json.dump(self.memory_store, f)
        except Exception as e:
            logger.error(f"Memory: Failed to save: {e}")

    def record_outcome(self, team_id: str, domain: str, strategy: str, result: Dict[str, Any], success: bool):
        """
        ARTICLE 316: Recording collective experiences.
        """
        entry = {
            "timestamp": datetime.now().isoformat(),
            "team_id": team_id,
            "domain": domain,
            "strategy": strategy,
            "result_summary": result.get("summary", "N/A"),
            "success": success,
            "fidelity": result.get("fidelity", 0.0),
            "efficiency": result.get("efficiency", 0.0)
        }
        self.memory_store.append(entry)
        self._save_memory()
        logger.info(f"Memory: Recorded VTF outcome for {team_id} ({domain}). Success: {success}")

    def query_best_strategies(self, domain: str, limit: int = 5) -> List[str]:
        """
        ARTICLE 316: Propagating successful patterns.
        Filters strategies by domain and success rate.
        """
        domain_memories = [m for m in self.memory_store if m["domain"] == domain]
        if not domain_memories:
            return ["STANDARD_PARALLEL_EXECUTION"]

        # Group by strategy and compute success rate
        strategies = {}
        for m in domain_memories:
            s = m["strategy"]
            if s not in strategies:
                strategies[s] = {"successes": 0, "total": 0}
            strategies[s]["total"] += 1
            if m["success"]:
                strategies[s]["successes"] += 1

        sorted_strategies = sorted(
            strategies.keys(),
            key=lambda k: (strategies[k]["successes"] / strategies[k]["total"]),
            reverse=True
        )
        return sorted_strategies[:limit]

    def get_insights(self) -> Dict[str, Any]:
        """Returns high-level statistics of collective learning."""
        total = len(self.memory_store)
        if total == 0:
            return {"total_experiences": 0}

        successes = sum(1 for m in self.memory_store if m["success"])
        return {
            "total_experiences": total,
            "global_success_rate": successes / total,
            "domains_covered": list(set(m["domain"] for m in self.memory_store))
        }
