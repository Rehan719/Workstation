import logging
from typing import Dict, Any, Optional
from agentic_core.biomimicry.geospheric.digital_twin_orchestrator import DigitalTwinOrchestrator
from agentic_core.change_control.reconfigulator import ConstitutionalReconfigulator
from agentic_core.genetic_immune.immune_system import ImmuneSystem
from agentic_core.mjm.twin_learner import MJMRecursiveLearner
from agents.coe_improvement import CoeImprovementAgent

logger = logging.getLogger(__name__)

class DigitalTwinController:
    """
    Lightweight facade that orchestrates the twin's self‑reflection,
    simulation, repair, and defence.
    """
    def __init__(self, orchestrator: Optional[DigitalTwinOrchestrator] = None):
        # Composition: Reuse validated homeostasis engine
        self.orchestrator = orchestrator or DigitalTwinOrchestrator()

        # Internal subsystems
        self.reconfigulator = self.orchestrator.reconfigulator
        self.immune = ImmuneSystem(self.orchestrator.constitutional_validator)
        self.meta_learner = self.orchestrator.mjm
        self.coe_agent = CoeImprovementAgent(
            self.orchestrator.constitutional_validator,
            self.orchestrator.ueg
        )

    async def step(self) -> Dict[str, Any]:
        """
        Execute one full cycle of the self-reflective digital twin.
        """
        logger.info("Executing Digital Twin self-reflection cycle.")

        # 1. Sync twin with live state, simulate, reflect and evolve
        # This is the core 'mind' of the twin
        evolution_report = await self.orchestrator.reflect_and_evolve()

        # 2. Scan for threats using immune system (enhanced with twin predictions)
        threats = await self.immune.scan_threats(self.orchestrator)

        # 3. Evaluate pending improvements via COE agent
        proposals = await self.reconfigulator.get_pending_proposals()
        evaluation_results = []
        for proposal in proposals:
            approved = await self.coe_agent.evaluate(proposal)
            evaluation_results.append({"proposal_id": proposal.get("id"), "approved": approved})

        # 4. Return consolidated state
        result = {
            "evolution": evolution_report,
            "threat_assessment": threats,
            "improvement_evaluations": evaluation_results,
            "system_health": self.orchestrator.live_state.get("system_health", 1.0)
        }

        return result
