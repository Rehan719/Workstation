"""The water cycle — the sixth, and the one that was shaped differently from the other five.

W544 (FU-355) — WHAT WAS WRONG HERE, measured. The other five cycles extend GeosphericCycle and define
sense(), so one implementation on the base class answers for all of them. This one did not:

  (a) IT EXTENDED NOTHING, so it inherited none of the three-state deviation(), is_homeostatic() or
      sense_reservoir() work — and the one cycle most likely to be read first (liquidity) was the one with
      no reading method at all. GET /api/v1/cycles had to report a stated absence for it.
  (b) IT DECLARED ITS OWN PIDController, a second copy of the controller in base_cycle.py with the same
      algorithm and no provenance fields — so the gains_tuned and gains_basis work did not exist on it. A
      second copy of control logic is a second place it can drift, which is the same rule as "no second
      store of numbers" applied to code rather than to data.
  (c) ITS SETPOINT OF 75.0 IS A TEMPERATURE and nothing said so. regulate_homeostasis(current_temp) is
      what reveals it. Meanwhile the binding this cycle now has measures LIQUIDITY IN VIRTUAL WST, so the
      two are incommensurable — which is exactly why W543's surface refused to compute a deviation. The
      unit is now DECLARED, so that refusal is computed from a mismatch rather than asserted by a rule.
  (d) evaporate() and condense() MUTATE the reservoirs using literal rates annotated as simulated, and
      self.efficiency = 0.85 multiplied the returned figure. They are a metaphor with no real subject on
      this platform: nothing calls them, and the reservoir dict they move is the same dict of literals the
      other five cycles were reporting as readings. They now return their figure WITH the literals named,
      so a caller cannot mistake a declared rate for a measured one.
"""
from .base_cycle import GeosphericCycle, PIDController

#  The literal rates this module has always used, named and given their provenance in one place rather
#  than inline where they read as findings. None of these is measured or tuned.
_MAX_EVAPORATION_RATE = 100.0
_CONDENSATION_RECOVERY = 0.9
_DECLARED_EFFICIENCY = 0.85
_LITERALS_BASIS = (
    f"DECLARED, NOT MEASURED: the evaporation cap ({_MAX_EVAPORATION_RATE}), the condensation recovery "
    f"fraction ({_CONDENSATION_RECOVERY}) and the efficiency ({_DECLARED_EFFICIENCY}) are literals carried "
    f"in this module since it was written. Nothing on this platform measured or tuned any of them")


class HydrologicManager(GeosphericCycle):
    """Thermal/liquidity analogue. Extends the shared cycle, uses the shared controller."""

    def __init__(self, cooling_system, ueg, validator):
        #  THE UNIT IS DECLARED. 75.0 is a temperature in the cooling metaphor — regulate_homeostasis
        #  below takes a current_temp — and saying so is what lets a surface decide for itself whether a
        #  deviation against a measured figure means anything.
        super().__init__(name="water", setpoint=75.0, tolerance=0.05,
                         setpoint_unit="degrees (cooling metaphor; not a currency or a volume)")
        #  THE SHARED CONTROLLER, not a second copy of it: this module declared its own PIDController
        #  class with the same algorithm and none of the provenance fields.
        self.pid = PIDController(setpoint=75.0, kp=1.2, ki=0.1, kd=0.5)
        self.cooling = cooling_system
        self.ueg = ueg
        self.validator = validator
        self.reservoirs = {"ocean": 97.0, "atmosphere": 0.001, "ice": 2.0, "groundwater": 0.6,
                           "surface": 0.3}
        self.efficiency = _DECLARED_EFFICIENCY

    async def sense(self) -> dict:
        #  The same honest reading as the other five: these reservoirs are literals nothing writes, so no
        #  figure and no verdict come out of them. The MEASURED binding for water is the ledger, reported
        #  by GET /api/v1/cycles.
        return await self.sense_reservoir("ocean_share", "ocean")

    async def regulate(self) -> dict:
        #  No measured temperature is available from anywhere, so this refuses rather than regulating
        #  towards a target from a reservoir literal. regulate_homeostasis(current_temp) remains the path
        #  for a caller that has actually measured one.
        return {"correction": None,
                "basis": ("NOT REGULATED: no measured temperature was supplied and nothing on this "
                          "platform reports one, so there is no error term. The reservoir literals in "
                          "this module are not a reading")}

    async def evaporate(self, heat_load: float) -> dict:
        """Move the metaphor's reservoirs from a caller-supplied heat load, with the literals named."""
        if hasattr(self.validator, "validate_thermal_operation"):
            await self.validator.validate_thermal_operation(heat_load)
        evap = min(heat_load, _MAX_EVAPORATION_RATE)
        self.reservoirs["atmosphere"] += evap
        self.reservoirs["ocean"] -= evap * 0.01
        if self.ueg:
            await self.ueg.log_event("water_evaporation", {"evaporation_rate": evap})
        #  A DICT, NOT A BARE FLOAT. The figure was `evap * self.efficiency` — a caller receiving that
        #  number had no way to know an untuned literal had been applied to it.
        return {"evaporated": evap, "returned": evap * self.efficiency,
                "efficiency_applied": self.efficiency, "basis": _LITERALS_BASIS}

    async def condense(self) -> dict:
        condensable = self.reservoirs["atmosphere"]
        reclaimed = condensable * _CONDENSATION_RECOVERY
        self.reservoirs["ocean"] += reclaimed
        self.reservoirs["atmosphere"] -= condensable
        if self.ueg:
            await self.ueg.log_event("water_condensation", {"reclaimed_energy": reclaimed})
        return {"reclaimed": reclaimed, "recovery_fraction": _CONDENSATION_RECOVERY,
                "basis": _LITERALS_BASIS}

    async def regulate_homeostasis(self, current_temp: float) -> dict:
        """The path for a caller that measured a temperature. Three-state, like the other five."""
        dev = self.deviation(current_temp)
        if dev is None:
            return {"correction": None, "status": "not_assessable",
                    "basis": ("NOT REGULATED: no measured temperature was supplied, so there is no error "
                              "term to act on")}
        error = self.pid.setpoint - current_temp
        correction = self.pid.compute(error)
        if dev > self.tolerance and self.ueg:
            await self.ueg.log_event("homeostasis_deviation",
                                     {"current_temp": current_temp, "setpoint": self.pid.setpoint,
                                      "deviation": round(dev, 6)})
        return {"correction": correction,
                "status": ("within_tolerance" if dev <= self.tolerance else "deviation"),
                "basis": (f"deviation {round(dev, 6)} of a supplied temperature against the setpoint "
                          f"{self.pid.setpoint} {self.setpoint_unit}; {self.pid.gains_basis}")}

    async def get_state(self) -> dict:
        return {"reservoirs": self.reservoirs, "setpoint": self.pid.setpoint,
                "setpoint_unit": self.setpoint_unit, "setpoint_is_aspiration": True,
                "literals_basis": _LITERALS_BASIS}
