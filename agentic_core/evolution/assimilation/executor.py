import logging
from typing import List, Dict, Any
from agentic_core.genome.chromosome import Chromosome
from .evaluator import AssimilationEvaluator

logger = logging.getLogger(__name__)

class AssimilationExecutor:
    """
    ARTICLE 165: Metamorphosis & Assimilation.
    Integrates successful evolutionary outcomes into the Workstation's core being.
    """
    def __init__(self, core_genome: Chromosome):
        self.core_genome = core_genome
        self.history: List[Dict[str, Any]] = []

    def assimilate(self, evolved_genome: Chromosome, evaluator: AssimilationEvaluator):
        """
        Executes phased integration of evolved features while preserving GRB integrity.
        """
        eval_result = evaluator.evaluate_fitness(evolved_genome)

        if not eval_result["compliant"]:
            logger.error("ASSIMILATION: Evolved genome failed compliance check. Aborting.")
            return False

        if not evaluator.validate_safety(evolved_genome):
            logger.error("ASSIMILATION: Safety validation failed. Aborting.")
            return False

        # Phased integration: Add new genes to core genome
        new_genes_count = 0
        for gene_id in evolved_genome.sequence:
            if gene_id not in self.core_genome.sequence:
                gene = evolved_genome.gene_map[gene_id]
                self.core_genome.add_gene(gene)
                new_genes_count += 1

        logger.info(f"ASSIMILATION: Integrated {new_genes_count} new genes into core genome.")
        self.history.append({
            "genes_added": new_genes_count,
            "status": "SUCCESS"
        })
        return True
