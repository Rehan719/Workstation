import json
import logging
import os
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class GenomicRegistry:
    """
    ARTICLE 1058: Epigenetic Trait Inheritance (v135.0).
    Stores serialized machine-readable traits (configurations, amendments) for inheritance.
    """
    def __init__(self, storage_path: str = "agentic_core/evolution/genomic_registry.json"):
        self.storage_path = storage_path
        self.traits = self._load_registry()

    def _load_registry(self) -> Dict[str, Any]:
        if os.path.exists(self.storage_path):
            with open(self.storage_path, "r") as f:
                return json.load(f)
        return {"traits": []}

    def encode_trait(self, trait_id: str, configuration: Dict[str, Any], effectiveness: float):
        """Serializes a successful configuration as a heritable trait."""
        trait = {
            "trait_id": trait_id,
            "version": "135.0.0",
            "effectiveness_score": effectiveness,
            "heritability": 0.85,
            "configuration": configuration,
            "metadata": {"origin": "sovereign_node_1", "status": "MATURE"}
        }
        self.traits["traits"].append(trait)
        self._save()
        logger.info(f"GenomicRegistry: Encoded trait '{trait_id}' with score {effectiveness}.")

    def inherit_top_traits(self) -> List[Dict[str, Any]]:
        """Returns top-scoring traits for initialization of new instances."""
        sorted_traits = sorted(self.traits["traits"], key=lambda x: x["effectiveness_score"], reverse=True)
        return sorted_traits[:5]

    def _save(self):
        with open(self.storage_path, "w") as f:
            json.dump(self.traits, f, indent=4)
