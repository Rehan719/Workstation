import logging
import uuid
from typing import Dict, Any, List

from agentic_core.orchestration.enterprise_organism_v66_1 import EnterpriseOrganismV66_1
from agentic_core.swarm.signaling_protocol import SignalingProtocol
from agentic_core.swarm.signal_types import SwarmSignal, SignalType
from agentic_core.swarm.orchestration_engine import OrchestrationEngine
from agentic_core.survival.swarm_meta_governor import SwarmMetaGovernor

logger = logging.getLogger(__name__)

class SwarmOrganismV67_0(EnterpriseOrganismV66_1):
    """
    v67.0: The Swarm-Capable Enterprise Organism.
    Backward compatible with v66.1 biological engine.
    """
    def __init__(self, agent_id: str = None):
        super().__init__()
        self.agent_id = agent_id or f"organism-{str(uuid.uuid4())[:8]}"
        self.signaling = SignalingProtocol(self.agent_id)
        self.swarm_orchestrator = OrchestrationEngine(self.agent_id, self.signaling)
        self.meta_governor = SwarmMetaGovernor()

        self._setup_swarm_handlers()
        self.signaling.start_listener()
        logger.info(f"SWARM_ORGANISM: Instance {self.agent_id} initialized.")

    def _setup_swarm_handlers(self):
        self.signaling.register_handler(SignalType.RECRUITMENT, self._handle_recruitment)
        self.signaling.register_handler(SignalType.ALARM, self._handle_alarm)

    def _handle_recruitment(self, signal: SwarmSignal):
        logger.info(f"SWARM: Received recruitment for {signal.payload['goal']}")
        # Automatically accept for simulation if not overloaded
        if self.meta_governor.swarm_allostatic_load < 7.0:
            logger.info("SWARM: Accepting task.")
            # Trigger internal enterprise cycle for the sub-task
            self.execute_strategic_cycle()

    def _handle_alarm(self, signal: SwarmSignal):
        logger.critical(f"SWARM: GLOBAL ALARM RECEIVED FROM {signal.sender_id}: {signal.payload['threat']}")
        # Trigger internal immune response
        self.immune_logic.sense("GlobalThreat")

    def execute_swarm_task(self, high_level_goal: str):
        """Orchestrates a task across the swarm if we are the leader."""
        logger.info(f"SWARM: Initiating collective workflow for: {high_level_goal}")
        tasks = self.swarm_orchestrator.decompose_goal(high_level_goal)
        self.swarm_orchestrator.assign_tasks()
        return tasks

    def shutdown(self):
        self.signaling.stop_listener()
        super().shutdown() if hasattr(super(), 'shutdown') else None
