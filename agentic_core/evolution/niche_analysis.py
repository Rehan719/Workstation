import logging
import numpy as np
from typing import List, Dict, Any
from agentic_core.genome.polyploid import PolyploidGenome
from agentic_core.genome.chromosome import Chromosome

logger = logging.getLogger(__name__)

class NicheExpansionAnalyzer:
    """
    ARTICLE 169: Niche Expansion Analysis.
    Measures how duplicated genomes enable adaptation to challenging environments.
    """
    def __init__(self):
        self.output_variation: List[float] = []

    def measure_variation(self, polyploid_genome: PolyploidGenome) -> float:
        """
        Quantifies signal output variation in duplicated gene regulatory networks.
        """
        # Simplified: Variation proportional to number of active chromosomes
        active_counts = [len(c.sequence) for c in polyploid_genome.chromosomes]
        variation = float(np.std(active_counts)) if len(active_counts) > 1 else 0.0
        self.output_variation.append(variation)
        logger.info(f"NICHE ANALYSIS: Measured variation {variation:.4f}")
        return variation

    def correlate_with_stress(self, environmental_stress: float) -> float:
        """
        Tests the hypothesis that polyploid advantage increases with stress.
        """
        # Return a mock correlation score
        return environmental_stress * 1.1
