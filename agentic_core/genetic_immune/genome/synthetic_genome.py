import hashlib
import logging
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)

class Gene:
    def __init__(self, name: str, function_hash: str, regulatory_elements: List[str]):
        self.name = name
        self.function_hash = function_hash
        self.regulatory_elements = regulatory_elements # Transcription factor binding sites

class SyntheticGenome:
    """
    DP: Synthetic Genome.
    Stores the complete set of potential behaviors (genes) and regulatory sequences.
    """
    def __init__(self):
        self.genes: Dict[str, Gene] = {}
        self.epigenome_state: Dict[str, float] = {} # Accessibility 0.0 to 1.0

    def register_gene(self, name: str, function_hash: str, regulatory_elements: List[str]):
        self.genes[name] = Gene(name, function_hash, regulatory_elements)
        self.epigenome_state[name] = 1.0 # Default accessible

    def transcribe(self, active_transcription_factors: List[str]) -> List[str]:
        """
        Determines which genes are expressed based on TFs and epigenetic state.
        """
        expressed_genes = []
        for name, gene in self.genes.items():
            # Check if any required regulatory element is in active TFs
            if any(tf in gene.regulatory_elements for tf in active_transcription_factors):
                if self.epigenome_state.get(name, 1.0) > 0.5:
                    expressed_genes.append(name)

        logger.debug(f"GENOME: Transcribing genes: {expressed_genes}")
        return expressed_genes
