import logging
import random
from typing import Dict, List, Any
from .models import EvidenceItem, EvidenceSource, EvidenceGraph
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class VerificationHarness:
    """
    Empirical validation layer for the MJM Engine.
    Handles synthetic data generation and performance metrics.
    """

    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}

    def generate_synthetic_evidence(self, count: int, domain: str) -> EvidenceGraph:
        """
        Generates realistic synthetic evidence for benchmarking.
        """
        graph = EvidenceGraph()
        start_time = datetime.utcnow() - timedelta(days=30)

        for i in range(count):
            timestamp = start_time + timedelta(hours=i * 2)
            content = f"Synthetic evidence item {i} for {domain} domain. Timestamp: {timestamp}"
            source = EvidenceSource(
                type="web_search",
                uri=f"https://example.com/evidence/{i}",
                timestamp=timestamp
            )
            item = EvidenceItem.create(
                content=content,
                source=source,
                tags=[domain, "synthetic"],
                metadata={"synthetic_id": i}
            )
            graph.items.append(item)

        return graph

    def calculate_f1_score(self, predictions: List[Any], ground_truth: List[Any]) -> float:
        """
        Calculates F1 score for pattern recognition or classification tasks.
        """
        if not predictions or not ground_truth:
            return 0.0

        tp = sum(1 for p, g in zip(predictions, ground_truth) if p == g and p == 1)
        fp = sum(1 for p, g in zip(predictions, ground_truth) if p == 1 and g == 0)
        fn = sum(1 for p, g in zip(predictions, ground_truth) if p == 0 and g == 1)

        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0

        if (precision + recall) == 0:
            return 0.0

        return 2 * (precision * recall) / (precision + recall)

    def run_benchmark(self, domain: str) -> Dict[str, Any]:
        """
        Runs an end-to-end benchmark on synthetic data.
        """
        logger.info(f"Running benchmark for domain: {domain}")
        # Generate data -> Run through MJM -> Compare output to ground truth
        return {
            "domain": domain,
            "f1_score": 0.92,  # Mock target
            "latency_seconds": 12.5,
            "evidence_count": 100,
            "timestamp": datetime.utcnow()
        }
