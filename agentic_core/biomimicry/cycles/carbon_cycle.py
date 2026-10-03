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
        #  W543 — this returned the reservoir literal and a homeostatic verdict computed from
        #  it. Nothing writes that reservoir, so the verdict described a quantity nobody had
        #  measured. One implementation, on the base class, now answers for all of them.
        return await self.sense_reservoir("current_load", "active_data")

    async def regulate(self) -> dict:
        #  W543 — this read self.reservoirs['active_data'], a literal nothing writes, and handed it to the
        #  PID as though it were a measurement. Passing None instead routes it to the one
        #  refusal below: regulate_homeostasis(value) remains the path for a caller that has
        #  actually measured something.
        return await self._regulate_with_val(None)

    async def regulate_homeostasis(self, current_load: float) -> float:
        """Standard interface for homeostatic regulation."""
        result = await self._regulate_with_val(current_load)
        return result["correction_applied"]

    async def _regulate_with_val(self, current_load: float) -> dict:
        #  W543 — THREE STATES. deviation() answers None when there is nothing to compare, and
        #  `dev <= self.tolerance` would raise a TypeError on it. Returning a refusal rather
        #  than raising keeps a governance outcome from reading as a malfunction.
        dev = self.deviation(current_load)
        if dev is None:
            return {"status": "not_assessable", "correction_applied": None,
                    "new_estimate": None,
                    "basis": ("NOT REGULATED: no measured value was supplied, so there is no "
                              "error term. A correction computed from a reservoir literal is "
                              "indistinguishable from a real one once it is reported")}
        error = self.pid.setpoint - current_load
        status = "within_tolerance" if dev <= self.tolerance else "deviation"

        correction = self.pid.compute(error)
        if self.storage and hasattr(self.storage, "adjust_metabolism"):
            self.storage.adjust_metabolism(correction)

        #  Same keys as the refusal above: a caller reading `basis` must not get undefined on
        #  the path that worked, or the only branch it can describe is the one that failed.
        return {
            "status": status,
            "correction_applied": correction,
            "new_estimate": current_load + (correction * 0.1),
            "basis": (f"deviation {round(dev, 6)} against tolerance {self.tolerance}; correction from "
                      f"a PID whose gains are {self.pid.gains_basis}")
        }
