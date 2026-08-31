import logging
from typing import Dict, Any
from src.organism.python.ai_gateway import gateway

logger = logging.getLogger(__name__)

class HybridOrchestrator:
    """
    Mixture-of-Experts Router.
    Decomposes complex tasks into subtasks for specialized models.
    """
    def __init__(self):
        self.gateway = gateway
        self.specializations = {
            "ingestion": "deepseek",
            "legal_reasoning": "qwen",
            "coding": "minimax",
            "general": "deepseek"
        }

    async def execute_task(self, prompt: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Decomposes the prompt and executes subtasks via specialized models.
        """
        # 1. Simple Decomposition Logic (Rule-based for v1)
        task_map = self._decompose(prompt)

        results = {}
        for task_name, model_pref in task_map.items():
            logger.info(f"HybridOrchestrator: Dispatching subtask '{task_name}' to {model_pref}")

            # Construct sub-prompt
            sub_prompt = [
                {"role": "system", "content": f"Execute the subtask: {task_name}"},
                {"role": "user", "content": prompt}
            ]

            # Execute via gateway (which handles caching/budgeting)
            results[task_name] = await self.gateway.execute_completion(model_pref, sub_prompt)

        # 2. Result Fusion
        final_output = self._fuse_results(results)

        return {
            "final_content": final_output,
            "subtasks": list(results.keys()),
            "orchestration_metadata": {"model_mapping": task_map}
        }

    def _decompose(self, prompt: str) -> Dict[str, str]:
        """Maps parts of a prompt to specialized providers."""
        mapping = {}
        lower_prompt = prompt.lower()

        if "code" in lower_prompt or "function" in lower_prompt:
            mapping["coding"] = self.specializations["coding"]

        if "legal" in lower_prompt or "tribunal" in lower_prompt:
            mapping["legal_research"] = self.specializations["legal_reasoning"]

        if not mapping:
            mapping["general"] = self.specializations["general"]

        return mapping

    def _fuse_results(self, results: Dict[str, Any]) -> str:
        """Combines multiple model outputs into a cohesive response."""
        if len(results) == 1:
            return list(results.values())[0]["content"]

        fused = "### Hybrid Intelligence Report\n\n"
        for task, res in results.items():
            fused += f"#### [{task.upper()}] (Provider: {res['provider']})\n"
            fused += res["content"] + "\n\n"

        return fused
