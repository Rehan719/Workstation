from typing import Any, Dict, List, Optional
from ..base_agent import BaseAgent

class DecisionAgent(BaseAgent):
    """
    PC-Agent: Decision Agent (DA)
    Executes low-level GUI or API interactions based on perceptions.
    """
    def __init__(self, agent_id: str = "pc_agent.decision.v10", config: Optional[Dict[str, Any]] = None):
        super().__init__(agent_id, config)

    async def execute(self, task: Dict[str, Any], context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        action = task.get("action")
        self.log(f"DA executing action: {action}")

        if action == "optimize_layout":
            return await self.tree_search_visual_choice(task.get("variants", []))

        return {"status": "executed", "action": action, "result": "success"}

    async def tree_search_visual_choice(self, variants: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Implementation of Paper2Video's Tree Search Visual Choice.
        Evaluates multiple layout variants and selects the best one using a VLM score.
        """
        self.log(f"Running Tree Search Visual Choice for {len(variants)} layout variants")

        best_variant = None
        highest_score = -1.0

        for variant in variants:
            # Simulate VLM Evaluation Score (normally this calls Gemini 2.5 Pro / GPT-4o-v)
            score = self._simulated_vlm_score(variant)
            self.log(f"Variant {variant.get('id')} scored: {score}")

            if score > highest_score:
                highest_score = score
                best_variant = variant

        return {
            "status": "optimized",
            "best_layout": best_variant,
            "score": highest_score
        }

    def _simulated_vlm_score(self, variant: Dict[str, Any]) -> float:
        """Heuristic for layout quality: balance, readability, and font size."""
        score = 0.5
        # Prefer layouts that don't overflow
        if not variant.get("overflow"):
            score += 0.3
        # Prefer layouts with higher font size
        score += variant.get("font_size", 12) / 100
        return min(1.0, score)
