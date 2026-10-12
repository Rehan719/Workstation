from typing import Dict, Any, Optional
from decimal import Decimal
from datetime import datetime, UTC
import hashlib

class BaseReactorAdapter:
    """Base class for all reactor adapters."""
    def __init__(self, reactor_name: str):
        self.reactor_name = reactor_name

    async def deploy_capital(self, amount: Decimal, strategy: str) -> Dict[str, Any]:
        """
        Deploy capital to the reactor.
        Returns an InvestmentReceipt.
        """
        # In Phase 1, we simulate reactor returns
        # In production, this would call reactor.generate_returns(amount)
        roi = self._simulate_roi()
        risk = self._simulate_risk()
        deployment_hash = hashlib.sha256(f"{self.reactor_name}{amount}{strategy}{datetime.now(UTC)}".encode()).hexdigest()

        return {
            "reactor": self.reactor_name,
            "amount": float(amount),
            "expected_roi": roi,
            "risk_score": risk,
            "deployment_hash": deployment_hash,
            "timestamp": datetime.now(UTC).isoformat(),
            "status": "ACTIVE"
        }

    def _simulate_roi(self) -> float:
        return 0.05 # 5% default

    def _simulate_risk(self) -> float:
        return 0.2 # 20% default

class ScienceReactorAdapter(BaseReactorAdapter):
    def __init__(self):
        super().__init__("Science")

    def _simulate_roi(self) -> float:
        return 0.12 # 12% for Science (AlphaFold/Ginkgo)

class LawReactorAdapter(BaseReactorAdapter):
    def __init__(self):
        super().__init__("Law")

    def _simulate_roi(self) -> float:
        return 0.08 # 8% for Law

class EducationReactorAdapter(BaseReactorAdapter):
    def __init__(self):
        super().__init__("Education")

class EmploymentReactorAdapter(BaseReactorAdapter):
    def __init__(self):
        super().__init__("Employment")
