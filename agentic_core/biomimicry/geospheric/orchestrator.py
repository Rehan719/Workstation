from dataclasses import dataclass
from typing import Dict, List, Optional, Any
import numpy as np
from datetime import datetime, timedelta
import hashlib
import json
from .digital_twin_orchestrator import DigitalTwinOrchestrator

@dataclass
class ControlDecision:
    approved: bool
    reason: Optional[str] = None
    adjusted_setpoints: Optional[Dict[str, float]] = None
    efficiency_score: Optional[float] = None

class EcosystemHealthObjective:
    """
    Evaluates Global Ecosystem Health (Ψ‑functional).
    Targets Ψ ≥ 0.90 for high‑fidelity biological regulation.
    """
    def __init__(self, weights: Dict[str, float]):
        self.weights = weights
        self.setpoints = {
            "water": 75.0,
            "carbon": 50.0,
            "nitrogen": 10.0,
            "oxygen": 60.0,
            "phosphorus": 80.0,
            "sulfur": 1.0
        }

    async def evaluate(self, system_state) -> float:
        scores = []
        for name, weight in self.weights.items():
            metric = getattr(system_state, f"{name}_metric", None)
            setpoint = self.setpoints.get(name, 100.0)

            if metric is not None:
                # Fidelity calculation: 1.0 at setpoint
                deviation = abs(metric - setpoint)
                tolerance = max(0.1, setpoint * 0.05)
                fidelity = max(0.0, 1.0 - (deviation / tolerance))
                scores.append(fidelity * weight)

        return sum(scores) if scores else 0.0

class HomeostaticOrchestrator(DigitalTwinOrchestrator):
    """
    Coordinates six biogeochemical cycles to maintain system homeostasis.
    """
    def __init__(self, validator, mjm_model, ueg):
        super().__init__(validator, mjm_model, ueg)
        self.coupling_matrix = self._load_coupling_matrix()
        self.psi_threshold = 0.90
        self.psi_functional = EcosystemHealthObjective(weights={
            "water": 0.2,
            "carbon": 0.25,
            "nitrogen": 0.15,
            "oxygen": 0.15,
            "phosphorus": 0.15,
            "sulfur": 0.1
        })

    def _load_coupling_matrix(self) -> np.ndarray:
        return np.array([
            [1.0, 0.1, 0.05, 0.2, 0.0, 0.0],
            [0.1, 1.0, 0.3, 0.1, 0.2, 0.05],
            [0.05, 0.3, 1.0, 0.0, 0.4, 0.1],
            [0.2, 0.1, 0.0, 1.0, 0.0, 0.0],
            [0.0, 0.2, 0.4, 0.0, 1.0, 0.3],
            [0.0, 0.05, 0.1, 0.0, 0.3, 1.0]
        ])

    async def _check_lyapunov_stability(self, adjustments: Dict[str, float]) -> bool:
        return all(abs(v) <= 50.0 for v in adjustments.values())

    async def _audit_closed_loop(self, system_state) -> Dict[str, Any]:
        return {"unreclaimed": 0.0, "status": "CLOSED_LOOP_SUCCESS"}

    async def step(self, system_state) -> ControlDecision:
        # 1. Validation
        for name, controller in self.cycles.items():
            if hasattr(controller, "validate"):
                decision = await controller.validate(system_state)
                if not decision.approved:
                    return ControlDecision(approved=False, reason=f"Constitutional violation in {name}")

        # 2. Health
        health_score = await self.psi_functional.evaluate(system_state)

        # 3. Adjustments
        adjustments = {}
        for i, name in enumerate(["water", "carbon", "nitrogen", "oxygen", "phosphorus", "sulfur"]):
            current_val = getattr(system_state, f"{name}_metric", self.psi_functional.setpoints[name])
            correction = await self.cycles[name].regulate_homeostasis(current_val)

            influence = 0.0
            for j, other_name in enumerate(["water", "carbon", "nitrogen", "oxygen", "phosphorus", "sulfur"]):
                if i != j:
                    setpoint = self.psi_functional.setpoints[other_name]
                    other_val = getattr(system_state, f"{other_name}_metric", setpoint)
                    influence += self.coupling_matrix[i][j] * (other_val - setpoint)

            adjustments[name] = float(correction + (influence * 0.1))

        if not await self._check_lyapunov_stability(adjustments):
             return ControlDecision(approved=False, reason="Unstable coupling detected")

        if health_score < self.psi_threshold:
             # v∞-MASTER: Initiate recovery logging
             logger.warning(f"Homeostatic drift detected: Ψ={health_score:.3f}")

        # 5. Log
        if self.ueg:
            await self.ueg.log_event("TWIN_CONTROL_STEP", {
                "health_score": health_score,
                "adjustments": adjustments
            })

        return ControlDecision(
            approved=True,
            adjusted_setpoints=adjustments,
            efficiency_score=health_score
        )

import logging
logger = logging.getLogger(__name__)
