import logging
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)

class PhylogenyTracker:
    """
    ARTICLE 168 & 169: Evolutionary Traceability.
    Reconstructs evolutionary history of successful lineages.
    """
    def __init__(self):
        self.lineage_tree: Dict[str, str] = {} # offspring_id -> parent_id
        self.mutation_logs: Dict[str, List[Dict[str, Any]]] = {} # org_id -> mutations

    def record_reproduction(self, offspring_id: str, parent_id: str):
        self.lineage_tree[offspring_id] = parent_id
        logger.debug(f"PHYLOGENY: Recorded {offspring_id} from {parent_id}")

    def record_mutation(self, org_id: str, mutation_type: str, selection_coeff: float):
        if org_id not in self.mutation_logs:
            self.mutation_logs[org_id] = []
        self.mutation_logs[org_id].append({
            "type": mutation_type,
            "s": selection_coeff
        })

    def get_ancestry(self, org_id: str) -> List[str]:
        ancestry = []
        current = org_id
        while current in self.lineage_tree:
            current = self.lineage_tree[current]
            ancestry.append(current)
        return ancestry
