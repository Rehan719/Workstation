import logging
from typing import Dict, List, Any

logger = logging.getLogger(__name__)

class TranscriptionFactor:
    """
    DB: Transcription Factor.
    Binds to promoters to activate or repress 'gene' (module) expression.
    """
    def __init__(self, name: str, affinity: float):
        self.name = name
        self.affinity = affinity

    def __repr__(self):
        return f"TranscriptionFactor({self.name}, affinity={self.affinity})"

class Promoter:
    """
    DB: Promoter Region.
    Evaluates transcription factor binding to determine expression level.
    """
    def __init__(self, gene_name: str, binding_sites: List[str]):
        self.gene_name = gene_name
        self.binding_sites = binding_sites

    def evaluate(self, active_factors: List[TranscriptionFactor]) -> float:
        """
        Calculates expression level based on bound factors.
        """
        score = 0.0
        for factor in active_factors:
            if factor.name in self.binding_sites:
                score += factor.affinity

        expression_level = min(1.0, score)
        logger.debug(f"GENETICS: Promoter for {self.gene_name} evaluated to {expression_level}")
        return expression_level

class TranscriptionalControl:
    """
    DB: Transcriptional Control System.
    Manages the overall expression state of the organism's genomic modules.
    """
    def __init__(self):
        self.promoters = {}
        self.active_factors = []

    def register_promoter(self, gene_name: str, binding_sites: List[str]):
        self.promoters[gene_name] = Promoter(gene_name, binding_sites)

    def activate_factor(self, factor: TranscriptionFactor):
        self.active_factors.append(factor)

    def get_expression_profile(self) -> Dict[str, float]:
        profile = {}
        for gene, promoter in self.promoters.items():
            profile[gene] = promoter.evaluate(self.active_factors)
        return profile
