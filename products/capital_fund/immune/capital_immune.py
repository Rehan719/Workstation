import asyncio
from typing import Dict, Any, List
from datetime import datetime, UTC
from agentic_core.genetic_immune.immune_system import ImmuneSystem
from agentic_core.genetic_immune.anomaly_scorer import RealTimeAnomalyScorer
from agentic_core.ueg.logger import VSBUEGLogger as UEGLogger
from agentic_core.genetic_immune.reconfigulator import ConstitutionalReconfigulator as Reconfigulator
from agentic_core.genetic_immune.regulator import Regulator
from agentic_core.governance.multisig_council import MultiSigCouncil

class CapitalImmuneSystem:
    """
    Module 2E: Genetic-Immune Self-Healing for the Capital Fund.
    Monitors drawdown via Hoshiyari (anomaly detection) and triggers
    emergency hedging and constitutional mutations.
    """
    def __init__(self, owner_uid: str, digital_twin: Any):
        self.owner_uid = owner_uid
        self.digital_twin = digital_twin
        self.ueg = UEGLogger()
        self.anomaly_detector = RealTimeAnomalyScorer()

        # Core immune system components
        self.immune_system = ImmuneSystem(
            validator=None, # In Phase 2, we focus on digital_twin synergy
            digital_twin=self.digital_twin,
            ueg=self.ueg
        )

        self.council = MultiSigCouncil(ueg=self.ueg)
        self.regulator = Regulator(ueg=self.ueg, multi_sig=self.council)
        self.reconfigulator = Reconfigulator(ueg=self.ueg, regulator=self.regulator)

        self.drawdown_threshold = 0.15 # 15% drawdown triggers immune response

    async def monitor_and_act(self, current_metrics: Dict[str, float]) -> Dict[str, Any]:
        """
        Monitors fund health and triggers immune response if drawdown exceeds 15%.
        """
        drawdown = current_metrics.get("drawdown", 0.0)
        anomaly_score = self.anomaly_detector.score_message({"drawdown": drawdown})

        status = "HEALTHY"
        response_triggered = False

        if drawdown > self.drawdown_threshold:
            status = "THREAT_DETECTED"
            response_triggered = True
            await self._trigger_immune_response(drawdown, anomaly_score)

        result = {
            "uid": self.owner_uid,
            "timestamp": datetime.now(UTC).isoformat(),
            "status": status,
            "drawdown": drawdown,
            "anomaly_score": anomaly_score,
            "immune_response_active": response_triggered
        }

        await self.ueg.log_event("CAPITAL_IMMUNE_SCAN", result)
        return result

    async def _trigger_immune_response(self, drawdown: float, anomaly_score: float):
        """
        Triggers emergency hedging and reconfigulator mutation proposal.
        """
        emergency_action = {
            "type": "EMERGENCY_HEDGE",
            "reason": "Drawdown limit exceeded",
            "drawdown": drawdown,
            "anomaly_score": anomaly_score,
            "timestamp": datetime.now(UTC).isoformat(),
            "actions": [
                "Pause all new internal reactor deployments",
                "Liquidate 20% of highest-volatility assets to cash",
                "Increase MultiSigCouncil alert level to SEVERE"
            ]
        }

        # 1. Log to UEG with high severity
        await self.ueg.log_event("IMMUNE_RESPONSE_TRIGGERED", emergency_action)

        # 2. Propose Constitutional Amendment if repeated violations
        # In Phase 2, we simulate the proposal check
        if drawdown > 0.20:
            await self.reconfigulator.propose_enhancement(
                enhancement_type="risk_limit_amendment",
                context={
                    "proposed_limit": 0.10,
                    "reason": "Repeated 20% drawdown breach"
                }
            )

        print(f"CRITICAL: Immune response triggered for {self.owner_uid}. Drawdown: {drawdown:.2f}")
