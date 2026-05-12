import logging
import random
import hashlib
import json
from typing import List, Dict, Any, Optional
from .gene import Gene, GeneType
from .regulatory_block import GenomicRegulatoryBlock

logger = logging.getLogger(__name__)

class Chromosome:
    """
    ARTICLE 161 & 166: The Linear Chromosome.
    Enforces conserved synteny and manages gene positioning.
    Enhanced for Jules vΩ∞-MASTER production readiness.
    """
    def __init__(self, chromosome_id: str, is_circular: bool = False):
        self.chromosome_id = chromosome_id
        self.is_circular = is_circular
        self.sequence: List[str] = []  # List of gene_ids
        self.gene_map: Dict[str, Gene] = {}
        self.grb_map: Dict[str, GenomicRegulatoryBlock] = {}
        self.position_map: Dict[str, int] = {}
        self.metadata: Dict[str, Any] = {}

    def add_gene(self, gene: Gene, position: Optional[int] = None):
        """Adds a gene to the chromosome at a specific or end position."""
        if position is None:
            position = len(self.sequence)

        if gene.gene_id in self.gene_map:
            logger.warning(f"Gene {gene.gene_id} already exists in chromosome {self.chromosome_id}. Overwriting.")
            if gene.gene_id in self.sequence:
                self.sequence.remove(gene.gene_id)

        self.sequence.insert(position, gene.gene_id)
        self.gene_map[gene.gene_id] = gene
        self._update_positions()

    def get_gene(self, gene_id: str) -> Optional[Gene]:
        """Retrieves a gene by its ID."""
        return self.gene_map.get(gene_id)

    def set_gene(self, gene_id: str, gene: Gene):
        """Sets or updates a gene in the chromosome."""
        if gene_id not in self.gene_map:
            self.add_gene(gene)
        else:
            self.gene_map[gene_id] = gene

    def add_regulatory_block(self, grb: GenomicRegulatoryBlock):
        """Adds a Genomic Regulatory Block (GRB) to the chromosome."""
        self.grb_map[grb.block_id] = grb

    def _update_positions(self):
        """Internal helper to refresh the position index."""
        self.position_map = {gene_id: i for i, gene_id in enumerate(self.sequence)}

    def validate_synteny(self, reference_order: List[str]) -> float:
        """Computes collinearity score against a reference order (0.0 to 1.0)."""
        if not reference_order:
            return 1.0

        matches = 0
        for i, gene_id in enumerate(reference_order):
            if i < len(self.sequence) and self.sequence[i] == gene_id:
                matches += 1
        return matches / len(reference_order)

    def mutate(self, rate: float = 0.01):
        """
        Performs random genetic mutations on the chromosome.
        ARTICLE 166: Regulated mutation for adaptive evolution.
        """
        for gene in self.gene_map.values():
            if random.random() < rate:
                # Simulate mutation by changing the sequence hash
                new_blob = f"{gene.sequence_hash}{random.random()}".encode()
                gene.sequence_hash = hashlib.sha256(new_blob).hexdigest()
                logger.info(f"Mutated gene {gene.gene_id} in chromosome {self.chromosome_id}")

    def crossover(self, other: 'Chromosome') -> 'Chromosome':
        """
        Performs genetic crossover with another chromosome.
        ARTICLE 166: Recombination for genetic diversity.
        """
        child_id = f"{self.chromosome_id}_x_{other.chromosome_id}_{random.randint(1000, 9999)}"
        child = Chromosome(child_id, is_circular=self.is_circular)

        # Simple single-point crossover of the sequence
        cutoff = random.randint(0, min(len(self.sequence), len(other.sequence)))

        new_sequence_ids = self.sequence[:cutoff] + other.sequence[cutoff:]

        for gene_id in new_sequence_ids:
            # Prefer gene from parent who contributed the sequence slot
            parent = self if gene_id in self.gene_map else other
            if gene_id in parent.gene_map:
                child.add_gene(parent.gene_map[gene_id])

        return child

    def to_dict(self) -> Dict[str, Any]:
        """Serializes the chromosome for UEG logging or persistence."""
        return {
            "chromosome_id": self.chromosome_id,
            "is_circular": self.is_circular,
            "sequence": self.sequence,
            "genes": {gid: self._gene_to_dict(g) for gid, g in self.gene_map.items()},
            "grbs": {bid: self._grb_to_dict(b) for bid, b in self.grb_map.items()},
            "metadata": self.metadata
        }

    def _gene_to_dict(self, gene: Gene) -> Dict[str, Any]:
        return {
            "gene_id": gene.gene_id,
            "gene_type": gene.gene_type.value,
            "sequence_hash": gene.sequence_hash,
            "expression_threshold": gene.expression_threshold,
            "promoters": gene.promoters,
            "enhancers": gene.enhancers,
            "fitness_contribution": gene.fitness_contribution
        }

    def _grb_to_dict(self, grb: GenomicRegulatoryBlock) -> Dict[str, Any]:
        return {
            "block_id": grb.block_id,
            "target_gene_id": grb.target_gene_id,
            "hcnes": grb.hcnes,
            "bystander_genes": grb.bystander_genes,
            "tad_boundary_predicted": grb.tad_boundary_predicted
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Chromosome':
        """Deserializes a chromosome from a dictionary."""
        chrom = cls(data["chromosome_id"], data.get("is_circular", False))
        chrom.metadata = data.get("metadata", {})

        # Restore genes
        gene_data_map = data.get("genes", {})
        for gid in data.get("sequence", []):
            if gid in gene_data_map:
                g_data = gene_data_map[gid]
                gene = Gene(
                    g_data["gene_id"],
                    GeneType(g_data["gene_type"]),
                    g_data["sequence_hash"],
                    g_data.get("expression_threshold", 0.5)
                )
                gene.promoters = g_data.get("promoters", [])
                gene.enhancers = g_data.get("enhancers", [])
                gene.fitness_contribution = g_data.get("fitness_contribution", 0.0)
                chrom.add_gene(gene)

        # Restore GRBs
        for bid, b_data in data.get("grbs", {}).items():
            grb = GenomicRegulatoryBlock(b_data["block_id"], b_data["target_gene_id"])
            grb.hcnes = b_data.get("hcnes", [])
            grb.bystander_genes = b_data.get("bystander_genes", [])
            grb.tad_boundary_predicted = b_data.get("tad_boundary_predicted", False)
            chrom.add_regulatory_block(grb)

        return chrom

    def validate_constitutionally(self, validator: Any) -> bool:
        """Hooks into constitutional validation gates (GaaS v4)."""
        if hasattr(validator, "validate_genome"):
            return validator.validate_genome(self.to_dict())
        return True # Default to pass if no validator provided
