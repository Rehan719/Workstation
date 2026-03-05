import logging
import random
from typing import List, Optional
from agentic_core.genome.chromosome import Chromosome

logger = logging.getLogger(__name__)

class Indel:
    """
    ARTICLE 163: Insertion and Deletion (Small-scale).
    Implements small-scale genomic variations (1-100 bp).
    """
    def __init__(self, rate: float = 1e-4):
        self.rate: float = rate

    def apply(self, sequence_hash: str) -> str:
        """Randomly inserts or deletes bits in the sequence string."""
        if random.random() >= self.rate:
            return sequence_hash

        chars = list(sequence_hash)
        if not chars: return sequence_hash

        mode = random.choice(["insert", "delete"])
        idx = random.randint(0, len(chars) - 1)
        length = random.randint(1, min(5, len(chars)))

        if mode == "delete":
            new_chars = chars[:idx] + chars[idx+length:]
            logger.debug(f"INDEL: Deleted {length} chars at {idx}")
        else:
            inserted = [random.choice("0123456789abcdef") for _ in range(length)]
            new_chars = chars[:idx] + inserted + chars[idx:]
            logger.debug(f"INDEL: Inserted {length} chars at {idx}")

        return "".join(new_chars)
