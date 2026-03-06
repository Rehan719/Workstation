import logging
import math
from typing import Dict, Any
from .threat_memory import ThreatMemory

logger = logging.getLogger(__name__)

class ImmuneSystemV2:
    """
    BY: Immune System with Threat Memory.
    Multi-layered defense with sigmoidal detection and persistent memory.
    """
    def __init__(self):
        self.memory = ThreatMemory()
        self.ic50_perplexity = 42.3 # BY-I

    def evaluate_threat(self, sample: Dict[str, Any]) -> float:
        # Layer 1: Memory Check
        sample_hash = hash(str(sample))
        if self.memory.is_known_threat(sample_hash):
            logger.warning("BY-II: Rapid threat recognition via memory.")
            return 1.0

        # Layer 2: Perceptual Mismatch Detection (CL-I)
        if sample.get("perceptual_mismatch"):
             logger.warning("IMMUNE: Sensory mismatch detected (Potential misinformation).")
             return 0.9

        # Layer 3: Perceptual Adversarial Detection (CL-II)
        if sample.get("adversarial_score", 0.0) > 0.8:
             logger.error("IMMUNE: Perceptual adversarial input detected.")
             return 1.0

        # Layer 4: Sigmoidal Detection (BY-I)
        perplexity = sample.get("perplexity", 0)
        k = 0.5
        score = 1.0 / (1.0 + math.exp(-k * (perplexity - self.ic50_perplexity)))

        if score > 0.8:
            logger.warning(f"IMMUNE RESPONSE: High threat detected ({score:.2f})")
            self.memory.remember_threat(sample_hash)

        return score

    def trigger_self_healing(self, logs: list):
        """BY-IV: Self-Healing processes."""
        logger.info("Initiating autonomous self-healing...")
        return True
