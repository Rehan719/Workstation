import asyncio
import logging
from agentic_core.governance.verifiable_governance import VGAEngine
from agentic_core.immune.immune_system import ImmuneSystemV2
from src.organism.python.neural.event_bus import AsyncEventBus
from src.organism.python.neural.event_types import (
    IntentGenerated, GovernanceValidated, ValidationResult
)

logger = logging.getLogger(__name__)

class NemoclawAdapter:
    """
    Immune System / Governance / CCO
    Wraps existing VGAEngine and ImmuneSystem for policy enforcement.
    """
    def __init__(self, vga_engine: VGAEngine, immune_system: ImmuneSystemV2, event_bus: AsyncEventBus):
        self.vga = vga_engine
        self.immune = immune_system
        self.event_bus = event_bus
        self.policy_version = "v1.0.0-sovereign"

    async def validate_action(self, intent_event: IntentGenerated) -> GovernanceValidated:
        """
        Validates an intent through multi-layered defense and governance engines.
        """
        intent = intent_event.intent
        action_data = intent.parameters
        action_id = intent_event.id

        logger.info(f"Nemoclaw: Validating intent {action_id} - Goal: {intent.goal}")

        loop = asyncio.get_event_loop()
        threat_score = await loop.run_in_executor(None, self.immune.evaluate_threat, action_data)

        if threat_score > 0.8:
            logger.warning(f"Nemoclaw: High threat score ({threat_score:.2f}) detected by Immune Layer.")
            result = ValidationResult(
                is_valid=False,
                reason=f"Immune Response: Threat score {threat_score:.2f} too high.",
                policy_version=self.policy_version
            )
            validation_event = GovernanceValidated(
                action_id=action_id,
                validation_result=result,
                priority=1,
                source="nemoclaw"
            )
            await self.event_bus.publish(validation_event)
            return validation_event

        vga_results = []
        for policy_name in ["purpose", "constitutional", "shariah", "magnificent_seven"]:
            valid = await loop.run_in_executor(None, self.vga.validate_action, policy_name, action_data)
            vga_results.append(valid)

        is_compliant = all(vga_results)

        if is_compliant:
            logger.info(f"Nemoclaw: Action {action_id} passed all governance checks.")
            attestation = "ZK_ATTEST_SUCCESS_SOVEREIGN"
            result = ValidationResult(
                is_valid=True,
                reason="Governance compliant",
                attestation=attestation,
                policy_version=self.policy_version
            )
        else:
            logger.warning(f"Nemoclaw: Action {action_id} REJECTED by governance policies.")
            result = ValidationResult(
                is_valid=False,
                reason="Failed governance compliance",
                policy_version=self.policy_version
            )

        validation_event = GovernanceValidated(
            action_id=action_id,
            validation_result=result,
            priority=2 if is_compliant else 1,
            source="nemoclaw"
        )

        await self.event_bus.publish(validation_event)
        return validation_event
