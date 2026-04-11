import logging
import asyncio
import numpy as np
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional, Tuple
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

class Strategy(BaseModel):
    id: str
    name: str
    description: str
    resource_requirements: Dict[str, float]
    expected_confidence_gain: float

class MetaCognitionReport(BaseModel):
    chosen_strategy: Strategy
    expected_improvement: float
    reasoning: str
    confidence: float
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class MetaCognitiveLoop:
    """
    Enables MJM to observe, evaluate, and improve its own cognitive processes.
    Uses reinforcement learning (simplified contextual bandit) for strategy selection.
    """

    def __init__(self, strategies: List[Strategy] = None):
        self.strategy_library = strategies or [
            Strategy(id="strat-rapid", name="Rapid Scan", description="Heuristic-based quick assessment", resource_requirements={"compute": 1}, expected_confidence_gain=0.6),
            Strategy(id="strat-standard", name="Standard Inquiry", description="Iterative search with validation", resource_requirements={"compute": 4}, expected_confidence_gain=0.85),
            Strategy(id="strat-deep", name="Exhaustive Research", description="Multi-branch deep dive", resource_requirements={"compute": 10}, expected_confidence_gain=0.95)
        ]
        self.performance_history: Dict[str, List[float]] = {s.id: [] for s in self.strategy_library}
        self.strategy_weights = {s.id: 1.0 for s in self.strategy_library}

    async def think_about_thinking(self, task_context: Dict[str, Any]) -> MetaCognitionReport:
        """Selects the optimal strategy for the current task context."""
        # 1. Self-observation: simple logic to choose based on urgency vs importance
        urgency = task_context.get("urgency", 0.5)
        complexity = task_context.get("complexity", 0.5)

        scores = []
        for strat in self.strategy_library:
            # Score = (Performance * weight) + (Exploration bonus)
            perf_avg = np.mean(self.performance_history[strat.id]) if self.performance_history[strat.id] else 0.5
            weight = self.strategy_weights[strat.id]

            # Simple heuristic matching
            match_score = 1.0
            if urgency > 0.8 and strat.id != "strat-rapid": match_score *= 0.5
            if complexity > 0.8 and strat.id == "strat-rapid": match_score *= 0.3

            final_score = (perf_avg * weight * match_score) + (0.1 * np.random.random())
            scores.append((strat, final_score))

        best_strategy, best_score = max(scores, key=lambda x: x[1])

        report = MetaCognitionReport(
            chosen_strategy=best_strategy,
            expected_improvement=best_score - 0.5,
            reasoning=f"Selected {best_strategy.name} based on task complexity ({complexity}) and urgency ({urgency}).",
            confidence=0.88
        )

        logger.info(f"MetaCognition: {report.reasoning}")
        return report

    async def evaluate_decision_outcome(self, strategy_id: str, actual_quality: float):
        """Updates strategy weights based on actual outcome quality."""
        if strategy_id in self.performance_history:
            self.performance_history[strategy_id].append(actual_quality)

            # Update weights: Reinforcement learning update
            baseline = 0.7
            reward = actual_quality - baseline
            self.strategy_weights[strategy_id] += 0.05 * reward

            logger.info(f"MetaCognition: Strategy {strategy_id} updated with reward {reward:.4f}. New weight: {self.strategy_weights[strategy_id]:.4f}")
