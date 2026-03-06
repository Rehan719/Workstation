import logging
from typing import Dict, List

logger = logging.getLogger(__name__)

class EpigeneticSystem:
    """
    Interface between rigid constitution and fluid behavior.
    Manages chromatin states (euchromatin/heterochromatin) and methylation.
    """
    def __init__(self, gene_names: List[str]):
        self.methylation: Dict[str, float] = {g: 0.1 for g in gene_names} # 0.0 (open) to 1.0 (silenced)
        self.chromatin: Dict[str, str] = {g: "euchromatin" for g in gene_names}

    def writer_mark(self, gene_name: str, mark_type: str, intensity: float):
        """Adds epigenetic marks."""
        if mark_type == "methylation":
            self.methylation[gene_name] = min(1.0, self.methylation[gene_name] + intensity)
            if self.methylation[gene_name] > 0.7:
                self.chromatin[gene_name] = "heterochromatin"
        logger.info(f"EPIGENETICS: Writer added {mark_type} to {gene_name}. State: {self.chromatin[gene_name]}")

    def eraser_mark(self, gene_name: str, mark_type: str, intensity: float):
        """Removes epigenetic marks."""
        if mark_type == "methylation":
            self.methylation[gene_name] = max(0.0, self.methylation[gene_name] - intensity)
            if self.methylation[gene_name] < 0.3:
                self.chromatin[gene_name] = "euchromatin"
        logger.info(f"EPIGENETICS: Eraser removed {mark_type} from {gene_name}. State: {self.chromatin[gene_name]}")

    def get_accessibility(self, gene_name: str) -> float:
        return 1.0 - self.methylation.get(gene_name, 0.0)
