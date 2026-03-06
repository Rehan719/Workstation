import logging
import random
from typing import Dict, Any
from agentic_core.genome.decoder import GenomeDecoder

logger = logging.getLogger(__name__)

class SelectionSystem:
    """
    ARTICLE 163 & 167: Selection Coefficient Computation.
    Selection coefficients emerge from comparative fitness, not predefined distributions.
    """
    def __init__(self, wild_type_fitness: float):
        self.wild_type_fitness = wild_type_fitness

    def compute_selection_coefficient(self, mutant_fitness: float) -> float:
        """
        s = (w_mutant / w_wild_type) - 1
        """
        if self.wild_type_fitness == 0:
            return 1.0 if mutant_fitness > 0 else 0.0

        s = (mutant_fitness / self.wild_type_fitness) - 1.0
        logger.debug(f"SELECTION: Mutant fitness {mutant_fitness:.4f} vs wild-type {self.wild_type_fitness:.4f}. s = {s:.4f}")
        return s

    def calculate_divergence(self, seq1: str, seq2: str) -> float:
        """Computes Hamming distance as a proxy for nucleotide divergence."""
        if not seq1 or not seq2:
            return 1.0

        mismatches = sum(c1 != c2 for c1, c2 in zip(seq1, seq2))
        max_len = max(len(seq1), len(seq2))
        return mismatches / max_len
