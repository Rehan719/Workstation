import logging
import math
from typing import Dict, Any, List
from .threat_memory import ThreatMemory

logger = logging.getLogger(__name__)

class ImmuneSystemV2:
    def __init__(self):
        self.memory = ThreatMemory()
        self.ic50_perplexity = 42.3

    def evaluate_threat(self, sample: Dict[str, Any]) -> float:
        sample_hash = hash(str(sample))
        if self.memory.is_known_threat(sample_hash): return 1.0
        if sample.get("type") == "cycle_anomaly":
            if sample.get("deviation", 0.0) > 0.4:
                self.memory.remember_threat(sample_hash)
                return 0.95
        if sample.get("adversarial_score", 0.0) > 0.8: return 1.0
        perplexity = sample.get("perplexity", 0)
        score = 1.0 / (1.0 + math.exp(-0.5 * (perplexity - self.ic50_perplexity)))
        if score > 0.8: self.memory.remember_threat(sample_hash)
        return score

    def generate_detector_vdj(self, cycle_patterns: List[str]) -> str:
        return f"VDJ-{hash(str(cycle_patterns))}"

    def trigger_self_healing(self, logs: list):
        return True
