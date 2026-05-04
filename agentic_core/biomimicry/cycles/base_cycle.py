from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Any, Optional

@dataclass
class PIDController:
    setpoint: float
    kp: float
    ki: float
    kd: float
    _integral: float = 0.0
    _last_error: float = 0.0

    def compute(self, current_value: float, dt: float = 1.0) -> float:
        error = self.setpoint - current_value
        self._integral += error * dt
        derivative = (error - self._last_error) / dt if dt > 0 else 0
        self._last_error = error
        return self.kp * error + self.ki * self._integral + self.kd * derivative

class CycleController:
    """Base class for twin's internal geospheric organs."""
    def __init__(self, name: str, setpoint: float, ueg: Any):
        self.name = name
        self.pid = PIDController(setpoint=setpoint, kp=1.0, ki=0.1, kd=0.2)
        self.ueg = ueg
        self.state = {"current": setpoint}

    async def get_state(self) -> Dict[str, Any]:
        return {"name": self.name, "value": self.state["current"], "setpoint": self.pid.setpoint}

    async def regulate(self, current_value: float):
        correction = self.pid.compute(current_value)
        self.state["current"] = current_value + correction
        await self.ueg.log_minimisation_event(f"{self.name}_regulation", {
            "correction": correction,
            "new_state": self.state["current"]
        })
        return correction
