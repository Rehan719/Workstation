from dataclasses import dataclass
from typing import Optional
import math
from datetime import datetime

@dataclass
class PIDController:
    """Proportional‑Integral‑Derivative controller for homeostatic regulation."""
    setpoint: float
    kp: float
    ki: float
    kd: float
    _integral: float = 0.0
    _last_error: float = 0.0
    _last_time: Optional[float] = None

    def compute(self, error: float, current_time: Optional[float] = None) -> float:
        """Compute control output based on error with anti‑windup."""
        if current_time is None:
            current_time = datetime.utcnow().timestamp()

        dt = (current_time - self._last_time) if self._last_time else 1.0
        self._last_time = current_time

        self._integral += error * dt
        # Anti‑windup: clamp integral term
        self._integral = max(-100, min(100, self._integral))

        derivative = (error - self._last_error) / dt if dt > 0 else 0
        self._last_error = error

        return (self.kp * error + self.ki * self._integral + self.kd * derivative)

class HydrologicManager:
    """Manages thermal resources via water cycle analogue – twin's self‑cooling organ."""
    def __init__(self, cooling_system, ueg, validator):
        self.pid = PIDController(setpoint=75.0, kp=1.2, ki=0.1, kd=0.5)
        self.cooling = cooling_system
        self.ueg = ueg
        self.validator = validator
        self.reservoirs = {
            "ocean": 97.0,
            "atmosphere": 0.001,
            "ice": 2.0,
            "groundwater": 0.6,
            "surface": 0.3
        }
        self.homeostasis_tolerance = 0.05

    async def evaporate(self, heat_load: float) -> float:
        """Convert computational heat to atmospheric moisture (self‑cooling)."""
        if hasattr(self.validator, "validate_thermal_operation"):
            await self.validator.validate_thermal_operation(heat_load)

        evap = min(heat_load, 100.0)
        self.reservoirs["atmosphere"] += evap
        self.reservoirs["ocean"] -= evap * 0.01

        if self.ueg:
            await self.ueg.log_event("water_evaporation", {
                "evaporation_rate": evap,
                "homeostasis": self._check_homeostasis("atmosphere")
            })
        return evap * 0.85

    async def regulate_homeostasis(self, current_temp: float) -> float:
        """Maintain system temperature within ±5% of setpoint via PID control."""
        error = self.pid.setpoint - current_temp
        correction = self.pid.compute(error)

        if self.ueg and abs(error) / self.pid.setpoint > self.homeostasis_tolerance:
            await self.ueg.log_event("homeostasis_deviation", {
                "cycle": "water",
                "error": error,
                "severity": "warning"
            })

        return correction

    def _check_homeostasis(self, reservoir: str) -> str:
        return "within_tolerance"

    async def get_state(self):
        return {"reservoirs": self.reservoirs, "temp": self.pid.setpoint}
