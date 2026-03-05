import logging
from typing import List, Dict, Any, Optional
from .gene import Gene

logger = logging.getLogger(__name__)

class GenomicRegulatoryBlock:
    """
    ARTICLE 161: Genomic Regulatory Blocks (GRBs).
    Indivisible evolutionary units containing target genes and HCNEs.
    """
    def __init__(self, block_id: str, target_gene_id: str):
        self.block_id = block_id
        self.target_gene_id = target_gene_id
        self.hcnes: List[str] = [] # Highly Conserved Non-coding Elements
        self.bystander_genes: List[str] = []
        self.tad_boundary_predicted: bool = False

    def add_hcne(self, hcne_id: str):
        self.hcnes.append(hcne_id)

    def add_bystander(self, gene_id: str):
        self.bystander_genes.append(gene_id)

    def validate_integrity(self) -> bool:
        """Ensures the block remains intact across versions."""
        return len(self.hcnes) > 0 and self.target_gene_id is not None
