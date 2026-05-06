from .base_cycle import PIDController, GeosphericCycle
from datetime import datetime

class NitrogenFixationDaemon(GeosphericCycle):
    """Manages task fixation via nitrogen cycle analogue."""
    def __init__(self, task_system, ueg, validator):
        super().__init__(name="nitrogen", setpoint=10.0, tolerance=0.05)
        self.pid = PIDController(setpoint=10.0, kp=0.8, ki=0.05, kd=0.1)
        self.task_system = task_system
        self.ueg = ueg
        self.validator = validator
        self.reservoirs = {
            "fixed_tasks": 0.0,
            "nitrified_tasks": 0.0,
            "denitrified_tasks": 0.0
        }

    async def sense(self) -> dict:
        return {
            "queue_depth": self.reservoirs["fixed_tasks"],
            "reservoirs": self.reservoirs.copy(),
            "homeostatic": self.is_homeostatic(self.reservoirs["fixed_tasks"])
        }

    async def regulate(self) -> dict:
        queue_depth = self.reservoirs["fixed_tasks"]
        return await self._regulate_with_val(queue_depth)

    async def regulate_homeostasis(self, queue_depth: float) -> float:
        result = await self._regulate_with_val(queue_depth)
        return result["correction_applied"]

    async def _regulate_with_val(self, queue_depth: float) -> dict:
        error = self.pid.setpoint - queue_depth
        dev = self.deviation(queue_depth)
        status = "within_tolerance" if dev <= self.tolerance else "deviation"

        correction = self.pid.compute(error)
        return {
            "status": status,
            "correction_applied": correction,
            "new_estimate": queue_depth + (correction * 0.1)
        }
