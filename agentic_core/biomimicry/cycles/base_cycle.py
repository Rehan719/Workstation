from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Any, Optional
from abc import ABC, abstractmethod

@dataclass
class PIDController:
    setpoint: float
    kp: float
    ki: float
    kd: float
    _integral: float = 0.0
    _last_error: float = 0.0
    _last_time: Optional[float] = None

    def compute(self, error: float, current_time: Optional[float] = None) -> float:
        """Compute control output based on error with anti-windup."""
        if current_time is None:
            current_time = datetime.utcnow().timestamp()

        dt = (current_time - self._last_time) if self._last_time else 1.0
        self._last_time = current_time

        self._integral += error * dt
        # Anti-windup: clamp integral term
        self._integral = max(-100, min(100, self._integral))

        derivative = (error - self._last_error) / dt if dt > 0 else 0
        self._last_error = error

        output = (self.kp * error +
                 self.ki * self._integral +
                 self.kd * derivative)
        return output

class GeosphericCycle(ABC):
    def __init__(self, name: str, setpoint: float, tolerance: float = 0.05):
        self.name = name
        self.setpoint = setpoint
        self.tolerance = tolerance
        self.reservoirs: dict = {}

    @abstractmethod
    async def sense(self) -> dict:
        """Return sensed metrics."""
        return {"cycle": self.name}

    @abstractmethod
    async def regulate(self) -> dict:
        """Apply homeostatic regulation."""
        return {"status": "ok"}

    def deviation(self, current: float) -> float:
        return abs(current - self.setpoint) / self.setpoint

    def is_homeostatic(self, current: float) -> bool:
        return self.deviation(current) <= self.tolerance

    async def get_state(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "setpoint": self.setpoint,
            "tolerance": self.tolerance,
            "reservoirs": self.reservoirs
        }

class CycleController(GeosphericCycle):
    """Legacy compatibility class."""
    def __init__(self, name: str, setpoint: float, ueg: Any):
        super().__init__(name, setpoint)
        self.pid = PIDController(setpoint=setpoint, kp=1.0, ki=0.1, kd=0.2)
        self.ueg = ueg
        self.state = {"current": setpoint}

    async def sense(self) -> dict:
        return {"value": self.state["current"]}

    async def regulate(self, current_value: float = None) -> dict:
        val = current_value if current_value is not None else self.state["current"]
        error = self.setpoint - val
        correction = self.pid.compute(error)
        self.state["current"] = val + correction
        if self.ueg:
            await self.ueg.log_minimisation_event(f"{self.name}_regulation", {
                "correction": correction,
                "new_state": self.state["current"]
            })
        return {"correction": correction}
