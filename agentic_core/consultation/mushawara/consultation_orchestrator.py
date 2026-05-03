import asyncio
import logging
import uuid
from typing import Any, Dict, List

from agentic_core.consultation.interface import (
    ConsultationRequest,
    ConsultationResponse,
    ValidationResult,
)
from agentic_core.consultation.uc_consult import UCIConsultHandler
from agentic_core.governance.gaas.gaas_validator import GaaSValidatorV4
from agentic_core.nemoclaw_runtime import NemoclawRuntime

from .perspective_aggregator import PerspectiveAggregator

logger = logging.getLogger("MushawaraOrchestrator")


class MushawaraOrchestrator:
    """
    Central Orchestrator for the Mushawara Consultation Bridge Engine.
    Manages multi-engine deliberation sessions, consensus tracking, and constitutional gating.
    """

    def __init__(
        self,
        gaas: GaaSValidatorV4,
        nemoclaw: NemoclawRuntime,
        uci_handler: UCIConsultHandler,
    ):
        self.gaas = gaas
        self.nemoclaw = nemoclaw
        self.uci = uci_handler
        self.aggregator = PerspectiveAggregator()
        self.active_sessions: Dict[str, Dict[str, Any]] = {}

    async def initiate_session(
        self,
        query: str,
        participants: List[str],
        context: Dict[str, Any] = {},
        domain: str = "general",
    ) -> ConsultationResponse:
        """
        Initiates and executes a full Mushawara deliberation session.
        """
        session_id = str(uuid.uuid4())
        logger.info(
            f"Mushawara: Initiating session {session_id} with participants: {participants}"
        )

        # 1. Global Pre-session Constitutional Check
        global_intent = {"type": "mushawara_session", "query": query, "domain": domain}
        gaas_res = await self.gaas.validate_intent(global_intent, context)
        if not gaas_res["passed"]:
            return ConsultationResponse(
                engine="mushawara_orchestrator",
                answer="Session blocked by global constitutional gate.",
                confidence=0.0,
                constitutional_validation=ValidationResult(
                    passed=False, violations=gaas_res.get("violations", [])
                ),
            )

        # 2. Parallel Consultation with Selected Participants
        consultation_tasks = []
        for engine in participants:
            req = ConsultationRequest(
                consultation_id=session_id,
                engine=engine,
                query=query,
                context=context,
                domain=domain,
            )
            consultation_tasks.append(self.uci.consult(req))

        responses: List[ConsultationResponse] = await asyncio.gather(
            *consultation_tasks
        )

        # 3. Perspective Synthesis & Consensus Aggregation (HD operations)
        synthesized_outcome = await self.aggregator.synthesize(responses, query)

        # 4. Final Constitutional Validation of Synthesized Outcome
        outcome_intent = {
            "type": "mushawara_outcome",
            "answer": synthesized_outcome.answer,
            "confidence": synthesized_outcome.confidence,
            "domain": domain,
        }
        final_gaas = await self.gaas.validate_intent(outcome_intent, context)

        synthesized_outcome.constitutional_validation = ValidationResult(
            passed=final_gaas["passed"],
            violations=final_gaas.get("violations", []),
            merkle_root=final_gaas.get("merkle_root"),
        )

        # 5. Log full session to UEG (via deliberation_logger implicitly in implementation)
        logger.info(
            f"Mushawara: Session {session_id} completed. Consensus: {synthesized_outcome.confidence:.2f}"
        )

        return synthesized_outcome
