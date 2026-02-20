from typing import Any, Dict

class ToolEvaluator:
    """
    Evaluates new tools against stability, performance, and license criteria.
    """
    async def evaluate_tool(self, tool: Dict[str, Any]) -> Dict[str, Any]:
        """
        Mock evaluation logic.
        """
        stability = 0.9 if tool["name"].endswith("v2") else 0.7
        performance = 0.85

        return {
            "stability_score": stability,
            "performance_score": performance,
            "license_compatible": tool["license"] in ["MIT", "Apache-2.0", "BSD-3-Clause"],
            "recommendation": "integrate" if stability > 0.8 else "watch"
        }
