import asyncio
from decimal import Decimal
from typing import Dict, Any, List
from agentic_core.mjm.hd_omni_learner import MJMv4OmniLearner as HDOmniLearner
from agentic_core.consultation.mushawara.consultation_orchestrator import ConsultationOrchestrator
from agentic_core.consultation.mushawara.perspective_aggregator import PerspectiveAggregator
from agentic_core.governance.gaas.gaas_validator import GaaSValidatorV4 as GaaSValidator
from products.capital_fund.vehicles.reactor_adapters import (
    ScienceReactorAdapter, LawReactorAdapter,
    EducationReactorAdapter, EmploymentReactorAdapter
)
from agentic_core.ueg.logger import VSBUEGLogger as UEGLogger

class InvestmentOrchestrator:
    """
    Orchestrates capital allocation across internal reactors.
    Uses MJM v4.0 for forecasting and Mushāwara for consensus.
    """
    def __init__(self):
        self.mjm = HDOmniLearner(dimension=10000)
        self.ueg = UEGLogger()
        self.validator = GaaSValidator(genome_path="config/constraints/absolute_constraints.yaml", legal_path="config/constraints/absolute_constraints.yaml")
        self.aggregator = PerspectiveAggregator(mjm_learner=self.mjm)
        self.mushawara = ConsultationOrchestrator(self.aggregator, self.ueg, self.validator)
        self.reactors = {
            "science": ScienceReactorAdapter(),
            "law": LawReactorAdapter(),
            "education": EducationReactorAdapter(),
            "employment": EmploymentReactorAdapter()
        }
        self.confidence_threshold = 0.85

    async def allocate_capital(self, uid: str, total_amount: Decimal) -> List[Dict[str, Any]]:
        """
        Allocates a total amount across reactors based on AI decisions.
        """
        # 1. Forecast returns using MJM (Simulated for Phase 1)
        forecast = await self._get_mjm_forecast(total_amount)
        if forecast["confidence"] < self.confidence_threshold:
            await self.ueg.log_event("ALLOCATION_REJECTED", {"reason": "Low MJM confidence", "confidence": forecast["confidence"]})
            return []

        # 2. Mushāwara Consultation (Simulated for Phase 1)
        consultation = await self._run_mushawara_consultation(forecast)
        if not consultation["approved"]:
            await self.ueg.log_event("ALLOCATION_REJECTED", {"reason": "Mushāwara rejected", "outcome": consultation})
            return []

        # 3. Execute Allocations
        deployments = []
        for reactor_name, weight in consultation["weights"].items():
            if reactor_name in self.reactors:
                amount = total_amount * Decimal(str(weight))
                receipt = await self.reactors[reactor_name].deploy_capital(amount, "auto_growth")
                deployments.append(receipt)

                await self.ueg.log_event("CAPITAL_DEPLOYED", {
                    "uid": uid,
                    "reactor": reactor_name,
                    "amount": float(amount),
                    "receipt": receipt
                }, merkle_link=True)

        return deployments

    async def _get_mjm_forecast(self, amount: Decimal) -> Dict[str, Any]:
        """Simulated MJM v4.0 forecast."""
        return {
            "confidence": 0.92,
            "expected_annual_return": 0.10,
            "risk_profile": "MODERATE"
        }

    async def _run_mushawara_consultation(self, forecast: Dict[str, Any]) -> Dict[str, Any]:
        """Simulated Mushāwara consultation."""
        return {
            "approved": True,
            "weights": {
                "science": 0.4,
                "law": 0.3,
                "education": 0.2,
                "employment": 0.1
            },
            "reasoning": "High confidence in Science reactor ROI; Law provides stable baseline."
        }
