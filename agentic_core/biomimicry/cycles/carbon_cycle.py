from .base_cycle import PIDController, GeosphericCycle
from datetime import datetime

class DataCarbonCycle(GeosphericCycle):
    """Manages data lifecycle via carbon cycle analogue – twin's metabolic organ."""
    def __init__(self, storage_system, ueg, validator):
        super().__init__(name="carbon", setpoint=50.0, tolerance=0.05)
        self.pid = PIDController(setpoint=50.0, kp=1.0, ki=0.1, kd=0.2)
        self.storage = storage_system
        self.ueg = ueg
        self.validator = validator
        self.reservoirs = {
            "active_data": 0.0,
            "archived_data": 0.0,
            "sequestration_pool": 0.0
        }

    async def sense(self) -> dict:
        return {
            "current_load": self.reservoirs["active_data"],
            "reservoirs": self.reservoirs.copy(),
            "homeostatic": self.is_homeostatic(self.reservoirs["active_data"])
        }

    async def regulate(self) -> dict:
        current_load = self.reservoirs["active_data"]
        return await self._regulate_with_val(current_load)

    async def regulate_homeostasis(self, current_load: float) -> float:
        """Standard interface for homeostatic regulation."""
        result = await self._regulate_with_val(current_load)
        return result["correction_applied"]

    async def _regulate_with_val(self, current_load: float) -> dict:
        error = self.pid.setpoint - current_load
        dev = self.deviation(current_load)
        status = "within_tolerance" if dev <= self.tolerance else "deviation"

        correction = self.pid.compute(error)
        if self.storage and hasattr(self.storage, "adjust_metabolism"):
            self.storage.adjust_metabolism(correction)

        return {
            "status": status,
            "correction_applied": correction,
            "new_estimate": current_load + (correction * 0.1)
        }
