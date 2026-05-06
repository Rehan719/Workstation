from .base_cycle import PIDController, GeosphericCycle
from datetime import datetime

class PhosphorusMemoryManager(GeosphericCycle):
    """Manages memory hierarchy via phosphorus cycle analogue."""
    def __init__(self, memory_system, ueg, validator):
        super().__init__(name="phosphorus", setpoint=80.0, tolerance=0.05)
        self.pid = PIDController(setpoint=80.0, kp=0.5, ki=0.01, kd=0.05)
        self.memory_system = memory_system
        self.ueg = ueg
        self.validator = validator
        self.reservoirs = {
            "available_phosphorus": 100.0,
            "sedimentation_pool": 0.0
        }

    async def sense(self) -> dict:
        return {
            "memory_pressure": self.reservoirs["sedimentation_pool"],
            "reservoirs": self.reservoirs.copy(),
            "homeostatic": self.is_homeostatic(self.reservoirs["sedimentation_pool"])
        }

    async def regulate(self) -> dict:
        mem_pressure = self.reservoirs["sedimentation_pool"]
        return await self._regulate_with_val(mem_pressure)

    async def regulate_homeostasis(self, mem_pressure: float) -> float:
        result = await self._regulate_with_val(mem_pressure)
        return result["correction_applied"]

    async def _regulate_with_val(self, mem_pressure: float) -> dict:
        error = self.pid.setpoint - mem_pressure
        dev = self.deviation(mem_pressure)
        status = "within_tolerance" if dev <= self.tolerance else "deviation"

        correction = self.pid.compute(error)
        return {
            "status": status,
            "correction_applied": correction,
            "new_estimate": mem_pressure + (correction * 0.1)
        }
