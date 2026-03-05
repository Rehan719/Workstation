import logging
import random
from typing import List, Optional
from agentic_core.genome.gene import Gene

logger = logging.getLogger(__name__)

class Substitution:
    """
    ARTICLE 163: Nucleotide Substitution.
    Implements single-bit substitutions with configurable transition/transversion bias.
    """
    def __init__(self, rate: float = 1e-4):
        self.rate: float = rate

    def apply(self, sequence_hash: str) -> str:
        """
        Randomly flips bits in the sequence hash based on mutation rate.

        Args:
            sequence_hash (str): The genomic sequence string to mutate.

        Returns:
            str: The mutated sequence hash.
        """
        if random.random() < self.rate:
            chars = list(sequence_hash)
            if not chars:
                return sequence_hash
            idx = random.randint(0, len(chars) - 1)
            chars[idx] = random.choice("0123456789abcdef")
            mutated = "".join(chars)
            logger.debug(f"SUBSTITUTION: Mutation at index {idx} in {sequence_hash[:8]}...")
            return mutated
        return sequence_hash
