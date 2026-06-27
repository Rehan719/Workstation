import logging
from typing import List, Dict, Any
from .chromosome import Chromosome
from .gene import Gene, GeneType

logger = logging.getLogger(__name__)

class GenomeDecoder:
    """
    ARTICLE 167: The Genotype-to-Phenotype Decoder.
    Inspired by Aevol, computes fitness from decoded genome function.
    """
    def __init__(self, chromosome: Chromosome):
        self.chromosome = chromosome
        self.active_phenotype: Dict[str, Any] = {}

    def decode_phenotype(self) -> Dict[str, Any]:
        """
        Translates chromosomal sequence into functional system behaviors.
        """
        phenotype = {
            "regulatory_density": 0.0,
            "structural_integrity": 1.0,
            "expressed_behaviors": []
        }

        reg_count = 0
        for gene_id in self.chromosome.sequence:
            gene = self.chromosome.gene_map.get(gene_id)
            if gene:
                if gene.gene_type == GeneType.REGULATORY:
                    reg_count += 1
                elif gene.gene_type == GeneType.STRUCTURAL:
                    phenotype["expressed_behaviors"].append(gene_id)

        phenotype["regulatory_density"] = reg_count / len(self.chromosome.sequence) if self.chromosome.sequence else 0.0
        self.active_phenotype = phenotype
        return phenotype

    def compute_fitness(self, environmental_target: Dict[str, Any]) -> float:
        """
        Calculates fitness by comparing active phenotype against environmental challenges.
        Selection coefficients emerge from this comparison.
        """
        if not self.active_phenotype:
            self.decode_phenotype()

        # Example fitness: match expressed behaviors to target
        target_behaviors = set(environmental_target.get("required_behaviors", []))
        actual_behaviors = set(self.active_phenotype.get("expressed_behaviors", []))

        if not target_behaviors:
            return 1.0

        intersection = actual_behaviors.intersection(target_behaviors)
        return len(intersection) / len(target_behaviors)
