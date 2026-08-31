import logging
from typing import Dict, Any, List
from src.organism.python.ai_gateway import gateway

logger = logging.getLogger(__name__)

class SelfCritiqueMiddleware:
    """
    Middleware for self-critique loops.
    Routes initial outputs to a secondary model for verification.
    """
    def __init__(self, primary_provider: str, critic_provider: str = "qwen"):
        self.primary = primary_provider
        self.critic = critic_provider

    async def execute_with_critique(self, messages: List[Dict[str, str]], **kwargs) -> Dict[str, Any]:
        """Executes completion and runs a critique loop if confidence is low."""
        # 1. Primary Inference
        initial_result = await gateway.execute_completion(self.primary, messages, **kwargs)
        content = initial_result["content"]

        # 2. Critique Request
        critique_prompt = [
            {"role": "system", "content": "You are a quality control agent. Critique the following AI output for factual errors and inconsistencies. Provide a score from 0-1."},
            {"role": "user", "content": f"AI Output to critique: {content}"}
        ]

        logger.info(f"SelfCritique: Requesting critique from {self.critic}...")
        critique_result = await gateway.execute_completion(self.critic, critique_prompt)

        # 3. Final Fusion
        return {
            "primary_content": content,
            "critique": critique_result["content"],
            "provider_info": {
                "primary": self.primary,
                "critic": self.critic
            }
        }
