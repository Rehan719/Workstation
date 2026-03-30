import logging
from typing import Dict, Any, List
from src.organism.python.ai_gateway import gateway

logger = logging.getLogger(__name__)

class MinimaxCoder:
    """
    Minimax-powered Codebase Assistant.
    Focus: Repository-aware context and autonomous test generation.
    """
    def __init__(self, provider: str = "minimax"):
        self.provider = provider

    async def suggest_refactor(self, code_snippet: str, context: str) -> Dict[str, Any]:
        """Suggests code refactoring based on snippet and context."""
        messages = [
            {"role": "system", "content": "You are an expert software engineer specialized in Python and biomimetic architectures."},
            {"role": "user", "content": f"Context: {context}\n\nRefactor this code for better async performance: {code_snippet}"}
        ]

        logger.info("MinimaxCoder: Generating refactor suggestions...")
        result = await gateway.execute_completion(self.provider, messages)

        return {
            "suggestion": result["content"],
            "risk_score": 0.3
        }

    async def generate_unit_test(self, function_code: str) -> str:
        """Generates a pytest unit test for the given function."""
        messages = [
            {"role": "system", "content": "Generate a robust pytest unit test for the following function."},
            {"role": "user", "content": function_code}
        ]

        result = await gateway.execute_completion(self.provider, messages)
        return result["content"]
