import asyncio
import logging
from agentic_core.ai_ceo.c_suite import BiomimeticCSuite
from src.organism.python.neural.event_bus import AsyncEventBus
from src.organism.python.neural.event_types import (
    IntentGenerated, StrategicIntent
)

logger = logging.getLogger(__name__)

class NematronAdapter:
    """
    Cognitive Core / Brain / CEO
    Wraps the existing BiomimeticCSuite to generate strategic intents.
    """
    def __init__(self, legacy_csuite: BiomimeticCSuite, event_bus: AsyncEventBus):
        self.legacy = legacy_csuite
        self.event_bus = event_bus
        self.source_id = "nematron"

    async def generate_intent(self, prompt: str) -> StrategicIntent:
        """
        Uses the multi-agent council to evaluate a proposal and generate a StrategicIntent.
        """
        logger.info(f"Nematron: Deliberating on proposal: {prompt}")

        loop = asyncio.get_event_loop()
        consensus = await loop.run_in_executor(None, self.legacy.reach_consensus, prompt)

        confidence = consensus.get("consensus_ratio", 0.0)
        verdict = consensus.get("verdict", False)

        intent = StrategicIntent(
            goal=prompt,
            action_type="COGNITIVE_DECISION",
            parameters={"verdict": verdict, "consensus": consensus.get("status")},
            reasoning=f"Council consensus reached with {confidence:.2f} ratio."
        )

        await self.event_bus.publish(IntentGenerated(
            source=self.source_id,
            intent=intent,
            confidence=confidence,
            priority=3
        ))

        return intent
