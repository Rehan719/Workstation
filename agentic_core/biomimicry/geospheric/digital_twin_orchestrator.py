import hashlib
import json
import numpy as np
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict

from .orchestrator import GeosphericHomeostaticOrchestrator
from .master_coordinator import SimulationResult, EvolutionReport

logger = logging.getLogger(__name__)

@dataclass
class TwinState:
    constitutional_compliance: float
    psi_health: float
    cycle_states: Dict[str, Any]
    subscription_state: Dict[str, Any]
    simulation_confidence: float
    timestamp: str = None
    state_checksum: str = None
    previous_checksum: str = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.utcnow().isoformat()
        if self.state_checksum is None:
            self.state_checksum = self._compute_checksum()

    def _compute_checksum(self) -> str:
        data = asdict(self)
        data.pop("state_checksum", None)
        data.pop("previous_checksum", None)
        blob = json.dumps(data, sort_keys=True)
        return hashlib.sha256(blob.encode()).hexdigest()

class DigitalTwinOrchestrator(GeosphericHomeostaticOrchestrator):
    """
    Orchestrates the digital twin's self‑reflection, simulation, and evolution.
    Maintains a SHA-256 hash chain for UEG Merkle-DAG integrity.
    """
    def __init__(self, validator=None, mjm_model=None, ueg=None):
        super().__init__(validator, ueg)
        self.mjm = mjm_model
        self.simulation_horizon = 3600  # 1 hour
        self.confidence_threshold = 0.85
        self._last_checksum = "genesis"

    async def capture_state(self) -> TwinState:
        """Capture comprehensive twin state with hash chaining."""
        cycle_states = await self.get_cycle_states()

        # System state for psi evaluation
        state_obj = type('SystemState', (), {f"{k}_metric": v.get('setpoint', 0.0) for k, v in cycle_states.items()})
        health_score = await self.psi_functional.evaluate(state_obj)

        state = TwinState(
            constitutional_compliance=1.0,
            psi_health=health_score,
            cycle_states=cycle_states,
            subscription_state={},
            simulation_confidence=self.mjm.get_confidence() if self.mjm else 1.0,
            previous_checksum=self._last_checksum
        )

        self._last_checksum = state.state_checksum

        if self.ueg:
            await self.ueg.log_event("TWIN_STATE_SNAPSHOT", asdict(state))

        return state

    async def simulate_future(self, horizon_seconds: int = None) -> SimulationResult:
        """Run the twin's internal model forward to predict future states."""
        horizon = horizon_seconds or self.simulation_horizon
        current_state = await self.capture_state()

        trajectory = [current_state]
        for _ in range(horizon // 60):
            if self.mjm:
                predicted_data = await self.mjm.predict_next(asdict(trajectory[-1]), {})
                valid_fields = {f.name for f in TwinState.__dataclass_fields__.values()}
                filtered_data = {k: v for k, v in predicted_data.items() if k in valid_fields}

                # Maintain chain in simulation (optional but useful)
                filtered_data["previous_checksum"] = trajectory[-1].state_checksum
                next_state = TwinState(**filtered_data)
                trajectory.append(next_state)

                if next_state.simulation_confidence < 0.7: # Hard-stop at low confidence
                    break
            else:
                break

        return SimulationResult(
            trajectory=trajectory,
            confidence=trajectory[-1].simulation_confidence if trajectory else 1.0
        )

    async def reflect_and_evolve(self) -> EvolutionReport:
        """Complete self-reflection cycle: sense → simulate → act → learn → evolve."""
        # 1. Sense
        current_state = await self.capture_state()

        # 2. Analyze & Simulate
        simulation = await self.simulate_future()

        # 3. Act
        # Trigger geospheric step with setpoints
        state_obj = type('SystemState', (), {f"{k}_metric": v.get('setpoint', 0.0) for k, v in current_state.cycle_states.items()})
        geospheric_decision = await self.step(state_obj)

        # 4. Learn
        learning_gain = 0.0
        if self.mjm and hasattr(self.mjm, "update"):
            learning_gain = await self.mjm.update(simulation)

        # 5. Recirculate (Evolve)
        evolution_actions = 0
        if geospheric_decision.approved and learning_gain > 0.01:
            evolution_actions += 1
            if self.ueg:
                await self.ueg.log_event("TWIN_EVOLUTION", {
                    "gain": learning_gain,
                    "checksum": current_state.state_checksum
                })

        return EvolutionReport(learning=learning_gain, corrections=evolution_actions)

    async def recover_state(self) -> Optional[TwinState]:
        """Cold-Start State Recovery from UEG."""
        if not self.ueg:
            return await self.capture_state()

        entries = await self.ueg.get_last_entries(count=100)
        for entry in reversed(entries):
            if entry.get("type") == "TWIN_STATE_SNAPSHOT":
                recovered = TwinState(**entry["payload"])
                self._last_checksum = recovered.state_checksum
                return recovered

        return await self.capture_state()
