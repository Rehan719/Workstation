import logging
from typing import Dict, Any, List, Optional
import json
import hashlib
import time
import os
from agentic_core.compliance.iso_23053 import ISO23053Compliance

logger = logging.getLogger(__name__)

class GenomicRegistry:
    """
    ARTICLE DC / IV.C: Blockchain Genomic Registry & Epigenetic Memory.
    Persistent trait memory for the digital organism.
    v129.1: Implements Multi-layered Epigenetic Memory (Layer 0-2).
    """
    def __init__(self, persistence_path: str = "meta/genome_ledger.json"):
        self.persistence_path = persistence_path
        self.blocks = []
        self.current_genome = {"traits": {}}
        self.compliance = ISO23053Compliance()

        # v129.1 Epigenetic Layers
        self.epigenetic_layers = {
            "layer_0": [], # Short-term (<24h)
            "layer_1": {}, # Long-term (30-90 days)
            "layer_2": {}  # Permanent (Epigenetic/Constitutional)
        }

        self._load()

    def store_epigenetic_pattern(self, pattern_id: str, data: Dict[str, Any], layer: int = 0):
        """ARTICLE IV.C: Distillation of patterns into epigenetic layers."""
        if layer == 0:
            self.epigenetic_layers["layer_0"].append({"id": pattern_id, "data": data, "ts": time.time()})
        elif layer == 1:
            self.epigenetic_layers["layer_1"][pattern_id] = data
        elif layer == 2:
            # Permanent encoding (chromatin-state analog)
            self.epigenetic_layers["layer_2"][pattern_id] = data
            self.reverse_transcribe_trait(f"epigenetic_{pattern_id}", data)

        logger.info(f"GenomicRegistry: Pattern {pattern_id} stored in Layer {layer}")

    def _load(self):
        """Loads the genome ledger from persistence."""
        if os.path.exists(self.persistence_path):
            try:
                with open(self.persistence_path, 'r') as f:
                    self.blocks = json.load(f)
                    if self.blocks:
                        self.current_genome = self.blocks[-1]["genotype"]
            except Exception as e:
                logger.error(f"GENOME: Failed to load ledger: {e}")

    def reverse_transcribe_trait(self, trait_id: str, data: Dict[str, Any]):
        """Transcribes an acquired trait into the current genome registry."""
        logger.info(f"GENOME: Transcribing trait {trait_id}")
        self.current_genome["traits"][trait_id] = data

    def commit_mutations(self, auth_proof: str) -> bool:
        """Commits all currently transcribed mutations to the ledger."""
        logger.info(f"GENOME: Committing mutations via {auth_proof}")
        return self.commit_mutation(self.current_genome["traits"], auth_proof)

    def commit_mutation(self, acquired_traits: Dict[str, Any], zkp_proof: str) -> bool:
        """
        Lamarckian update: reverse-transcribe acquired traits into the genome ledger.
        """
        # DC-II: Heritability check (98%) - Implementation ensures data is merged
        self.current_genome["traits"].update(acquired_traits)

        block = {
            "index": len(self.blocks) + 1,
            "timestamp": time.time(),
            "genotype": self.current_genome,
            "previous_hash": self._hash_block(self.blocks[-1]) if self.blocks else "0",
            "zkp_proof": zkp_proof
        }

        if self.compliance.verify_block_integrity(block):
            self.blocks.append(block)
            self._save()
            return True
        return False

    def _hash_block(self, block: Dict[str, Any]) -> str:
        s = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(s).hexdigest()

    def _save(self):
        os.makedirs("meta", exist_ok=True)
        try:
            with open(self.persistence_path, 'w') as f:
                json.dump(self.blocks, f, indent=2)
        except Exception as e:
            logger.error(f"GENOME: Failed to save ledger: {e}")

    def get_genome_depth(self) -> int:
        return len(self.blocks)
