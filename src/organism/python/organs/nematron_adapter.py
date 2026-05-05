import asyncio
import logging
from typing import Optional, List, Dict, Any
from agentic_core.ai_ceo.c_suite import BiomimeticCSuite
from src.organism.python.neural.event_bus import AsyncEventBus
from src.organism.python.neural.event_types import (
    IntentGenerated, StrategicIntent, BiomimeticEvent
)
from src.organism.python.ai_gateway import AIGateway

logger = logging.getLogger(__name__)

class NematronAdapter:
    """
    Cognitive Core / Brain / CEO
    Wraps the existing BiomimeticCSuite to generate strategic intents.
    """
    def __init__(self, legacy_csuite: BiomimeticCSuite, event_bus: AsyncEventBus, ai_gateway: Optional[AIGateway] = None):
        self.legacy = legacy_csuite
        self.event_bus = event_bus
        self.ai_gateway = ai_gateway
        self.source_id = "nematron"

        # Multi-agent C-Suite mapping for Hybrid MoE
        self.agent_specializations = {
            "CFO": "deepseek",  # Economics/Reasoning
            "CLO": "qwen",      # Legal/Compliance
            "CTO": "minimax",   # Code/Tech
            "CGO": "qwen",      # Governance
            "CISO": "minimax"   # Security
        }

    async def generate_intent(self, prompt: str) -> StrategicIntent:
        """
        Uses the multi-agent council to evaluate a proposal and generate a StrategicIntent.
        """
        logger.info(f"Nematron: Deliberating on proposal: {prompt}")

        loop = asyncio.get_event_loop()
        consensus = await loop.run_in_executor(None, self.legacy.reach_consensus, prompt)

        confidence = consensus.get("consensus_ratio", 0.0)
        verdict = consensus.get("verdict", False)

        # Article 1051: Enhanced C-Suite Deliberation logic using Hybrid MoE
        deliberation_logs = []
        if self.ai_gateway:
            deliberation_logs = await self._perform_ai_deliberation(prompt, consensus.get("votes", []))

        intent = StrategicIntent(
            goal=prompt,
            action_type="COGNITIVE_DECISION",
            parameters={
                "verdict": verdict,
                "consensus": consensus.get("status"),
                "deliberation_logs": deliberation_logs
            },
            reasoning=f"Council consensus reached with {confidence:.2f} ratio. {len(deliberation_logs)} agents used AI augmentation."
        )

        await self.event_bus.publish(IntentGenerated(
            source=self.source_id,
            intent=intent,
            confidence=confidence,
            priority=3
        ))

        return intent

    async def _perform_ai_deliberation(self, prompt: str, votes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Enhances council votes with AI-driven reasoning from specialized models.
        """
        logs = []
        tasks = []

        for vote in votes:
            agent_name = vote["agent"]
            if agent_name in self.agent_specializations:
                provider = self.agent_specializations[agent_name]
                tasks.append(self._get_agent_reasoning(agent_name, provider, prompt, vote["vote"]))

        if tasks:
            results = await asyncio.gather(*tasks, return_exceptions=True)
            for res in results:
                if isinstance(res, dict):
                    logs.append(res)
                else:
                    logger.error(f"Nematron: AI Deliberation error: {res}")

        return logs

    async def _get_agent_reasoning(self, agent: str, provider: str, prompt: str, vote: bool) -> Dict[str, Any]:
        """Queries a specialized model for an agent's reasoning."""
        messages = [
            {"role": "system", "content": f"You are the {agent} of a Sovereign AI Organism. Provide your specialized reasoning for the following proposal. Your initial vote was {'YES' if vote else 'NO'}."},
            {"role": "user", "content": prompt}
        ]

        try:
            # AIGateway handles provider selection, token budget, and neural bus signaling
            result = await self.ai_gateway.execute_completion(provider, messages)
            return {
                "agent": agent,
                "provider": provider,
                "reasoning": result.get("content", "No reasoning provided."),
                "status": "AUGMENTED"
            }
        except Exception as e:
            return {"agent": agent, "status": "ERROR", "error": str(e)}
