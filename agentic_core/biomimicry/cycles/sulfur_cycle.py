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
        #  W543 — this returned the reservoir literal and a homeostatic verdict computed from
        #  it. Nothing writes that reservoir, so the verdict described a quantity nobody had
        #  measured. One implementation, on the base class, now answers for all of them.
        return await self.sense_reservoir("error_rate", "error_volcano")

    async def regulate(self) -> dict:
        #  W543 — this read self.reservoirs['error_volcano'], a literal nothing writes, and handed it to the
        #  PID as though it were a measurement. Passing None instead routes it to the one
        #  refusal below: regulate_homeostasis(value) remains the path for a caller that has
        #  actually measured something.
        return await self._regulate_with_val(None)

    async def regulate_homeostasis(self, error_rate: float) -> float:
        result = await self._regulate_with_val(error_rate)
        return result["correction_applied"]

    async def _regulate_with_val(self, error_rate: float) -> dict:
        #  W543 — THREE STATES. deviation() answers None when there is nothing to compare, and
        #  `dev <= self.tolerance` would raise a TypeError on it. Returning a refusal rather
        #  than raising keeps a governance outcome from reading as a malfunction.
        dev = self.deviation(error_rate)
        if dev is None:
            return {"status": "not_assessable", "correction_applied": None,
                    "new_estimate": None,
                    "basis": ("NOT REGULATED: no measured value was supplied, so there is no "
                              "error term. A correction computed from a reservoir literal is "
                              "indistinguishable from a real one once it is reported")}
        error = self.pid.setpoint - error_rate
        status = "within_tolerance" if dev <= self.tolerance else "deviation"

        correction = self.pid.compute(error)
        #  Same keys as the refusal above: a caller reading `basis` must not get undefined on
        #  the path that worked, or the only branch it can describe is the one that failed.
        return {
            "status": status,
            "correction_applied": correction,
            "new_estimate": error_rate + (correction * 0.1),
            "basis": (f"deviation {round(dev, 6)} against tolerance {self.tolerance}; correction from "
                      f"a PID whose gains are {self.pid.gains_basis}")
        }
