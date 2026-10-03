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
        #  W543 — this returned the reservoir literal and a homeostatic verdict computed from
        #  it. Nothing writes that reservoir, so the verdict described a quantity nobody had
        #  measured. One implementation, on the base class, now answers for all of them.
        return await self.sense_reservoir("cpu_utilization", "metabolic_demand")

    async def regulate(self) -> dict:
        #  W543 — this read self.reservoirs['metabolic_demand'], a literal nothing writes, and handed it to the
        #  PID as though it were a measurement. Passing None instead routes it to the one
        #  refusal below: regulate_homeostasis(value) remains the path for a caller that has
        #  actually measured something.
        return await self._regulate_with_val(None)

    async def regulate_homeostasis(self, cpu_util: float) -> float:
        result = await self._regulate_with_val(cpu_util)
        return result["correction_applied"]

    async def _regulate_with_val(self, cpu_util: float) -> dict:
        #  W543 — THREE STATES. deviation() answers None when there is nothing to compare, and
        #  `dev <= self.tolerance` would raise a TypeError on it. Returning a refusal rather
        #  than raising keeps a governance outcome from reading as a malfunction.
        dev = self.deviation(cpu_util)
        if dev is None:
            return {"status": "not_assessable", "correction_applied": None,
                    "new_estimate": None,
                    "basis": ("NOT REGULATED: no measured value was supplied, so there is no "
                              "error term. A correction computed from a reservoir literal is "
                              "indistinguishable from a real one once it is reported")}
        error = self.pid.setpoint - cpu_util
        status = "within_tolerance" if dev <= self.tolerance else "deviation"

        correction = self.pid.compute(error)
        #  Same keys as the refusal above: a caller reading `basis` must not get undefined on
        #  the path that worked, or the only branch it can describe is the one that failed.
        return {
            "status": status,
            "correction_applied": correction,
            "new_estimate": cpu_util + (correction * 0.1),
            "basis": (f"deviation {round(dev, 6)} against tolerance {self.tolerance}; correction from "
                      f"a PID whose gains are {self.pid.gains_basis}")
        }
