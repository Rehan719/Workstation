from dataclasses import dataclass
from typing import Dict, Any, Optional
from datetime import datetime
from agentic_core.biomimicry.cycles.utils import constitutional_guard

@dataclass
class PIDController:
    """Proportional-Integral-Derivative controller for geospheric homeostasis."""
    setpoint: float
    kp: float
    ki: float
    kd: float
    _integral: float = 0.0
    _last_error: float = 0.0
    _last_time: Optional[float] = None

    def compute(self, error: float, current_time: Optional[float] = None) -> float:
        now = current_time or datetime.utcnow().timestamp()
        dt = (now - self._last_time) if self._last_time else 1.0
        self._last_time = now
        self._integral = max(-100.0, min(100.0, self._integral + error * dt))
        derivative = (error - self._last_error) / dt if dt > 0 else 0.0
        self._last_error = error
        return (self.kp * error) + (self.ki * self._integral) + (self.kd * derivative)

class DataCarbonCycle:
    """
    Models Data Lifecycle as the Carbon Cycle.
    Analogues: Photosynthesis (Ingestion), Respiration (Processing), Burial (Archival).
    """
    def __init__(self, storage_system, ueg, validator):
        self.pid = PIDController(setpoint=0.70, kp=1.0, ki=0.05, kd=0.2) # Target 70% utilization
        self.storage = storage_system
        self.ueg = ueg
        self.validator = validator
        self.reservoirs = {
            "biomass": 100.0,    # Active data
            "atmosphere": 50.0,   # Temporary/In-flight
            "ocean": 200.0,       # Near-line storage
            "lithosphere": 500.0  # Cold archival
        }
        self.homeostasis_tolerance = 0.05

    @constitutional_guard
    async def get_state(self) -> Dict[str, Any]:
        utilization = self.reservoirs["biomass"] / (self.reservoirs["biomass"] + self.reservoirs["ocean"] + self.reservoirs["lithosphere"])
        return {
            "utilization": utilization,
            "reservoirs": self.reservoirs.copy(),
            "within_tolerance": abs(utilization - self.pid.setpoint) <= self.homeostasis_tolerance
        }

    @constitutional_guard
    async def photosynthesize(self, raw_data_gain: float):
        """Data ingestion: Atmosphere -> Biomass."""
        await self.validator.validate_data_ingestion(raw_data_gain)
        self.reservoirs["atmosphere"] -= raw_data_gain * 0.1
        self.reservoirs["biomass"] += raw_data_gain
        await self.ueg.log_minimisation_event("carbon_photosynthesis", {"gain": raw_data_gain})
        return True

    @constitutional_guard
    async def respire(self, data_utilization: float):
        """Data processing: Biomass -> Atmosphere."""
        self.reservoirs["biomass"] -= data_utilization * 0.05
        self.reservoirs["atmosphere"] += data_utilization * 0.05
        await self.ueg.log_minimisation_event("carbon_respiration", {"utilization": data_utilization})
        return True

    @constitutional_guard
    async def regulate_homeostasis(self, current_utilization: float) -> float:
        """Maintains data utilization within ±5% of setpoint."""
        error = self.pid.setpoint - current_utilization
        correction = self.pid.compute(error)

        # Apply closed-loop transformation (e.g., archival or cleanup)
        if correction < 0: # Over utilization, move to lithosphere (burial)
            move_amt = abs(correction) * 10.0
            self.reservoirs["biomass"] -= move_amt
            self.reservoirs["lithosphere"] += move_amt

        await self.ueg.log_minimisation_event("carbon_homeostasis_correction", {
            "error": error,
            "correction": correction,
            "utilization": current_utilization
        })
        return correction
