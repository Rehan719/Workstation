from .base_cycle import PIDController, GeosphericCycle
from datetime import datetime

class SulfurErrorManager(GeosphericCycle):
    """Manages error signaling via sulfur cycle analogue."""
    def __init__(self, error_system, ueg, validator):
        super().__init__(name="sulfur", setpoint=1.0, tolerance=0.05)
        self.pid = PIDController(setpoint=1.0, kp=2.0, ki=0.5, kd=1.0)
        self.error_system = error_system
        self.ueg = ueg
        self.validator = validator
        self.reservoirs = {
            "error_volcano": 0.0,
            "sulfate_aerosols": 0.0
        }

    async def sense(self) -> dict:
        return {
            "error_rate": self.reservoirs["error_volcano"],
            "reservoirs": self.reservoirs.copy(),
            "homeostatic": self.is_homeostatic(self.reservoirs["error_volcano"])
        }

    async def regulate(self) -> dict:
        error_rate = self.reservoirs["error_volcano"]
        return await self._regulate_with_val(error_rate)

    async def regulate_homeostasis(self, error_rate: float) -> float:
        result = await self._regulate_with_val(error_rate)
        return result["correction_applied"]

    async def _regulate_with_val(self, error_rate: float) -> dict:
        error = self.pid.setpoint - error_rate
        dev = self.deviation(error_rate)
        status = "within_tolerance" if dev <= self.tolerance else "deviation"

        correction = self.pid.compute(error)
        return {
            "status": status,
            "correction_applied": correction,
            "new_estimate": error_rate + (correction * 0.1)
        }
