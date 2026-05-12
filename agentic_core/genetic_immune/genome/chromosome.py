import logging
from typing import List, Dict, Any, Optional
from .gene import Gene
from .regulatory_block import GenomicRegulatoryBlock

logger = logging.getLogger(__name__)

class Chromosome:
    """
    ARTICLE 161 & 166: The Linear Chromosome.
    Enforces conserved synteny and manages gene positioning.
    """
    def __init__(self, chromosome_id: str, is_circular: bool = False):
        self.chromosome_id = chromosome_id
        self.is_circular = is_circular
        self.sequence: List[str] = [] # List of gene_ids or element_ids
        self.gene_map: Dict[str, Gene] = {}
        self.grb_map: Dict[str, GenomicRegulatoryBlock] = {}
        self.position_map: Dict[str, int] = {}

    def add_gene(self, gene: Gene, position: Optional[int] = None):
        if position is None:
            position = len(self.sequence)
        self.sequence.insert(position, gene.gene_id)
        self.gene_map[gene.gene_id] = gene
        self._update_positions()

    def add_regulatory_block(self, grb: GenomicRegulatoryBlock):
        self.grb_map[grb.block_id] = grb

    def _update_positions(self):
        for i, gene_id in enumerate(self.sequence):
            self.position_map[gene_id] = i

    def validate_synteny(self, reference_order: List[str]) -> float:
        """Computes collinearity score against a reference order."""
        matches = 0
        for i, gene_id in enumerate(reference_order):
            if i < len(self.sequence) and self.sequence[i] == gene_id:
                matches += 1
        return matches / len(reference_order) if reference_order else 1.0
