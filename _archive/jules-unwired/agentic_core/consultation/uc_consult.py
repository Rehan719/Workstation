import logging
from typing import Any, Optional

from agentic_core.governance.gaas.gaas_validator import GaaSValidatorV4

from .interface import ConsultationRequest, ConsultationResponse, ValidationResult

logger = logging.getLogger("UCI_Consult")


class UCIConsultHandler:
    """
    Unified Consultation Interface (UCI-Consult) Handler.
    Orchestrates individual engine consultations with Nemoclaw and GaaS v4 integration.
    """

    def __init__(self, gaas: Optional[GaaSValidatorV4] = None):
        self.gaas = gaas
        # Nemoclaw runtime would be initialized here once implemented
        self.engines = {}  # Mapping of engine names to instances

    def register_engine(self, name: str, engine_instance: Any):
        """Registers a cognitive engine instance that implements the consult method."""
        self.engines[name] = engine_instance

    async def consult(self, request: ConsultationRequest) -> ConsultationResponse:
        """
        Routes a consultation request to the specified engine with pre/post-execution validation.
        """
        logger.info(f"UCI-Consult: Request received for engine {request.engine}")

        # 1. Pre-execution Constitutional Gating (GaaS v4)
        if self.gaas:
            # We wrap the request in an intent-like structure for the existing GaaSValidatorV4
            intent = {
                "type": "consultation_request",
                "engine": request.engine,
                "query": request.query,
                "domain": request.domain,
            }
            context = request.context
            gaas_result = await self.gaas.validate_intent(intent, context)
            if not gaas_result["passed"]:
                logger.error(
                    f"UCI-Consult: Pre-execution validation failed for engine {request.engine}"
                )
                return ConsultationResponse(
                    engine=request.engine,
                    answer="Consultation blocked by GaaS constitutional gate.",
                    confidence=0.0,
                    constitutional_validation=ValidationResult(
                        passed=False,
                        violations=gaas_result.get("violations", []),
                        merkle_root=gaas_result.get("merkle_root"),
                    ),
                )

        # 2. Engine Execution
        engine_instance = self.engines.get(request.engine)
        if not engine_instance:
            raise ValueError(f"Engine {request.engine} not registered in UCI-Consult.")

        try:
            # All engines are mandated to implement the async consult(request) -> ConsultationResponse interface
            response = await engine_instance.consult(request)
        except Exception as e:
            logger.exception(
                f"UCI-Consult: Engine {request.engine} execution error: {str(e)}"
            )
            return ConsultationResponse(
                engine=request.engine,
                answer=f"Internal engine error: {str(e)}",
                confidence=0.0,
                constitutional_validation=ValidationResult(
                    passed=False, violations=["ENGINE_EXECUTION_FAILURE"]
                ),
            )

        # 3. Post-execution Validation (Nemoclaw / GaaS v4)
        if self.gaas:
            outcome_intent = {
                "type": "consultation_outcome",
                "engine": request.engine,
                "answer": response.answer,
                "confidence": response.confidence,
            }
            outcome_gaas_result = await self.gaas.validate_intent(
                outcome_intent, request.context
            )
            if not outcome_gaas_result["passed"]:
                logger.error(
                    f"UCI-Consult: Post-execution validation failed for engine {request.engine}"
                )
                response.constitutional_validation = ValidationResult(
                    passed=False,
                    violations=outcome_gaas_result.get("violations", []),
                    merkle_root=outcome_gaas_result.get("merkle_root"),
                )

        return response
