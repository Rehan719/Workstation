import logging
from typing import List, Dict, Any, Optional
from enum import Enum

logger = logging.getLogger(__name__)

class GeneType(Enum):
    REGULATORY = "regulatory"
    STRUCTURAL = "structural"
    BYSTANDER = "bystander"

class Gene:
    """
    ARTICLE 161: The Gene Model.
    Distinguishes between regulatory and structural components.
    """
    def __init__(self,
                 gene_id: str,
                 gene_type: GeneType,
                 sequence_hash: str,
                 expression_threshold: float = 0.5):
        self.gene_id = gene_id
        self.gene_type = gene_type
        self.sequence_hash = sequence_hash
        self.expression_threshold = expression_threshold
        self.promoters: List[str] = []
        self.enhancers: List[str] = []
        self.fitness_contribution: float = 0.0

    def add_regulatory_element(self, element_id: str, is_promoter: bool = True):
        if is_promoter:
            self.promoters.append(element_id)
        else:
            self.enhancers.append(element_id)

    def __repr__(self):
        return f"Gene({self.gene_id}, {self.gene_type.value})"
