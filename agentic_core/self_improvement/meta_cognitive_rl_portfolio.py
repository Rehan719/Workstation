import logging
from typing import Dict, Any, List
from .complexity_scorer import ComplexityScorer
from .degradation_detector import PerformanceDegradationDetector
from .engagement_scorer import UserEngagementScorer
from .novelty_assessor import DomainNoveltyAssessor
from .weighted_adjuster import WeightedRatioAdjuster
from .rl_optimizer import RLPolicyOptimizer

logger = logging.getLogger(__name__)

class MetaCognitiveRLPortfolio:
    """
    ARTICLE CQ: Context-Aware Meta-Cognitive RL Portfolio.
    Dynamically adjusts the 70/30 capability/innovation split.
    """
    def __init__(self):
        self.complexity = ComplexityScorer()
        self.degradation = PerformanceDegradationDetector()
        self.engagement = UserEngagementScorer()
        self.novelty = DomainNoveltyAssessor()
        self.adjuster = WeightedRatioAdjuster()
        self.optimizer = RLPolicyOptimizer()
        self.baseline_innovation = 0.3

    def compute_optimal_split(self, context: Dict[str, Any]) -> float:
        """CQ-V: Weighted Adjustment Formula."""
        # 1. Gather scores (-1 to +1)
        scores = {
            "complexity": self.complexity.score(context.get('workload')),
            "degradation": self.degradation.detect(context.get('telemetry')),
            "engagement": self.engagement.score(context.get('user_signals')),
            "novelty": self.novelty.assess(context.get('domain_data'))
        }

        # 2. Compute innovation percentage
        # New_Innovation_Percentage = 0.3 + Σ(score_i × weight_i)
        innovation_pct = self.adjuster.calculate(self.baseline_innovation, scores)

        # CQ-VI: RL Policy Optimization
        self.optimizer.log_decision(context, scores, innovation_pct)

        logger.info(f"CQ: Meta-Cognitive RL set innovation split to {innovation_pct*100:.1f}%")
        return innovation_pct
