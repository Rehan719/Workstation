import logging
from typing import List, Dict, Any, Optional
from .chromosome import Chromosome
from .gene import Gene

logger = logging.getLogger(__name__)

class PolyploidGenome:
    """
    ARTICLE 169: Polyploidy & Duplication.
    Supports duplicated genomes for investigation of adaptive potential.
    """
    def __init__(self, baseline_chromosome: Chromosome, copies: int = 2):
        self.chromosomes: List[Chromosome] = [baseline_chromosome]
        self.copies = copies
        self.ortholog_fate: Dict[str, str] = {} # gene_id -> "active", "inactivated", "subfunctionalized"

        if copies > 1:
            self._duplicate_genome()

    def _duplicate_genome(self):
        """Creates copies of the baseline chromosome."""
        baseline = self.chromosomes[0]
        for i in range(1, self.copies):
            new_chrom = Chromosome(f"{baseline.chromosome_id}_copy_{i}")
            new_chrom.sequence = list(baseline.sequence)
            new_chrom.gene_map = dict(baseline.gene_map)
            new_chrom.grb_map = dict(baseline.grb_map)
            self.chromosomes.append(new_chrom)
        logger.info(f"Genome duplicated: {self.copies}x polyploidy established.")

    def model_re_diploidization(self, inactivation_rate: float = 0.1):
        """Simulates the loss of redundant gene copies over time."""
        # Simple model: randomly mark copies as inactivated
        import random
        for chrom in self.chromosomes[1:]:
            for gene_id in list(chrom.sequence):
                if random.random() < inactivation_rate:
                    chrom.sequence.remove(gene_id)
                    self.ortholog_fate[gene_id] = "inactivated"
