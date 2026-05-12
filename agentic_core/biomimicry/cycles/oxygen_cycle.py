from .base_cycle import PIDController, GeosphericCycle
from datetime import datetime

class MetabolicScheduler(GeosphericCycle):
    """Manages CPU scaling via oxygen cycle analogue."""
    def __init__(self, cpu_system, ueg, validator):
        super().__init__(name="oxygen", setpoint=60.0, tolerance=0.05)
        self.pid = PIDController(setpoint=60.0, kp=1.5, ki=0.2, kd=0.3)
        self.cpu_system = cpu_system
        self.ueg = ueg
        self.validator = validator
        self.reservoirs = {
            "oxygen_level": 100.0,
            "metabolic_demand": 0.0
        }

    async def sense(self) -> dict:
        return {
            "cpu_utilization": self.reservoirs["metabolic_demand"],
            "reservoirs": self.reservoirs.copy(),
            "homeostatic": self.is_homeostatic(self.reservoirs["metabolic_demand"])
        }

    async def regulate(self) -> dict:
        cpu_util = self.reservoirs["metabolic_demand"]
        return await self._regulate_with_val(cpu_util)

    async def regulate_homeostasis(self, cpu_util: float) -> float:
        result = await self._regulate_with_val(cpu_util)
        return result["correction_applied"]

    async def _regulate_with_val(self, cpu_util: float) -> dict:
        error = self.pid.setpoint - cpu_util
        dev = self.deviation(cpu_util)
        status = "within_tolerance" if dev <= self.tolerance else "deviation"

        correction = self.pid.compute(error)
        return {
            "status": status,
            "correction_applied": correction,
            "new_estimate": cpu_util + (correction * 0.1)
        }
