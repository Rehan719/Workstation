from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Any, Optional
from abc import ABC, abstractmethod

@dataclass
class PIDController:
    """A real PID — the integral is accumulated with anti-windup and the derivative is computed.

    W543 — worth stating because the register said otherwise: FU-326 reported that no PID exists anywhere
    in the geospheric package, which is true of agentic_core/biomimicry/geospheric/ and NOT true here.
    What is false is the architecture's claim that this controller is what runs: nothing on the UCI
    interception path reaches it, and no live module imports any of the six cycles that hold one.

    THE GAINS ARE DEFAULTS UNTIL TUNED, and now they say so. Six cycles carried six different hardcoded
    triples (water 1.2/0.1/0.5, carbon 1.0/0.1/0.2, nitrogen 0.8/0.05/0.1, oxygen 1.5/0.2/0.3,
    phosphorus 0.5/0.01/0.05, sulfur 2.0/0.5/1.0) with no provenance field anywhere, while three outside
    specifications each assert DIFFERENT "immutable" gains for the same six cycles. A gain presented
    without its origin reads as derived, and none of these was.
    """
    setpoint: float
    kp: float
    ki: float
    kd: float
    _integral: float = 0.0
    _last_error: float = 0.0
    _last_time: Optional[float] = None
    #  False until a tuning procedure has run against this platform's own data and recorded its result.
    #  No tuning is performed by this round; claiming otherwise is the defect this field exists to stop.
    gains_tuned: bool = False
    gains_basis: str = ("DEFAULT, NOT TUNED: these gains are literals carried in the cycle module that "
                        "constructed this controller. No tuning procedure has run against this "
                        "platform's data, so they are a starting point and not a derived setting")

    def compute(self, error: float, current_time: Optional[float] = None) -> float:
        """Compute control output based on error with anti-windup."""
        if current_time is None:
            current_time = datetime.utcnow().timestamp()

        dt = (current_time - self._last_time) if self._last_time else 1.0
        self._last_time = current_time

        self._integral += error * dt
        # Anti-windup: clamp integral term
        self._integral = max(-100, min(100, self._integral))

        derivative = (error - self._last_error) / dt if dt > 0 else 0
        self._last_error = error

        output = (self.kp * error +
                 self.ki * self._integral +
                 self.kd * derivative)
        return output

class GeosphericCycle(ABC):
    def __init__(self, name: str, setpoint: float, tolerance: float = 0.05,
                 setpoint_unit: Optional[str] = None):
        self.name = name
        self.setpoint = setpoint
        self.tolerance = tolerance
        #  W544 — THE UNIT, DECLARED OR ADMITTED ABSENT. W543 found that comparing a cycle's measured
        #  figure to its setpoint produced arithmetically sound nonsense — a liquidity of 900 virtual WST
        #  against water's setpoint of 75.0, which water_cycle.regulate_homeostasis(current_temp) shows to
        #  be a temperature — and refused every deviation with a blanket rule. A blanket rule is an
        #  assertion; this field lets the surface COMPUTE the refusal instead, by comparing the unit a
        #  setpoint declares against the unit the binding measures in. None means no unit was ever stated,
        #  which is the honest answer for five of the six and is not the same as a mismatch.
        self.setpoint_unit = setpoint_unit
        self.reservoirs: dict = {}

    @abstractmethod
    async def sense(self) -> dict:
        """Return sensed metrics."""
        return {"cycle": self.name}

    @abstractmethod
    async def regulate(self) -> dict:
        """Apply homeostatic regulation."""
        return {"status": "ok"}

    def deviation(self, current: Optional[float]) -> Optional[float]:
        """The fractional deviation from the setpoint, or None when there is nothing to compare.

        W543 — TWO WAYS THIS REPORTED A NUMBER IT HAD NO RIGHT TO. (a) It was two-state: given None it
        raised, so every caller passed whatever its reservoir dict held — and those dicts are literals
        set in __init__ that nothing ever writes. carbon's active_data is 0.0 against a setpoint of 50.0,
        so sense() reported a deviation of 1.0: a 100% departure from target, presented as a measurement,
        for a quantity nobody had measured. (b) It divided by self.setpoint with no guard, so a setpoint
        of 0 raised ZeroDivisionError from inside what reads like a pure accessor.

        A deviation from an unmeasured variable is not a deviation, and per this item's body a deviation
        from an aspiration is never reported as performance.
        """
        if not isinstance(current, (int, float)):
            return None
        if not self.setpoint:
            return None
        return abs(current - self.setpoint) / self.setpoint

    def is_homeostatic(self, current: Optional[float]) -> Optional[bool]:
        """True, False, or None for 'cannot be assessed' — never a default.

        The None case is the one that matters: it used to be impossible to express, so an unbound cycle
        had to answer the question one way or the other, and answering it either way is a claim.
        """
        dev = self.deviation(current)
        if dev is None:
            return None
        return dev <= self.tolerance

    async def sense_reservoir(self, metric: str, key: str) -> Dict[str, Any]:
        """The shared honest sense(): a reservoir literal is not a reading, so no verdict comes from it.

        W543 — all five cycles that defined sense() returned the same three things: a metric read
        straight out of self.reservoirs, a copy of that dict, and `homeostatic` computed from it. The
        reservoirs are literals assigned in __init__ that NOTHING in this repository ever writes
        (measured: no live module imports any of these classes, and no method writes the keys that
        sense() reads). carbon's active_data is 0.0 against a setpoint of 50.0, so the honest-looking
        answer was `homeostatic: False` — a precise verdict of failure, derived by real arithmetic, about
        a quantity nobody had measured. A false negative is not better than a false positive here; both
        are claims.

        The metric key is OMITTED rather than set to None, because a null invites `metric ?? 0` and the
        zero is the fabrication coming straight back. What the metric WOULD be is named instead.
        """
        raw = self.reservoirs.get(key)
        return {
            "metric": metric,
            "assessable": False,
            #  the explicit third state of the verdict, which is_homeostatic can now express
            "homeostatic": None,
            "reservoir_literal": raw,
            "reservoirs": dict(self.reservoirs),
            "basis": (f"NOT ASSESSED: this cycle's {metric} is read from self.reservoirs[{key!r}], which "
                      f"is a literal set in __init__ that nothing ever writes, so {raw!r} is a "
                      f"source-code value and not a reading. No deviation and no homeostatic verdict "
                      f"follow from it. The MEASURED binding for this cycle — or the reader that would "
                      f"bind it — is reported by GET /api/v1/cycles"),
        }

    async def get_state(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "setpoint": self.setpoint,
            "tolerance": self.tolerance,
            #  a setpoint with no unit is an aspiration, and this is the accessor that used to present
            #  it beside its reservoirs as though the two were comparable
            "setpoint_is_aspiration": True,
            "reservoirs": self.reservoirs
        }

class CycleController(GeosphericCycle):
    """Legacy compatibility class.

    W543 — `self.state = {"current": setpoint}` MADE EVERY FRESH CONTROLLER PERFECT. It seeded the
    current value with the target, so sense() reported the setpoint, deviation() computed exactly 0.0 and
    is_homeostatic() returned True — for a controller that had never read anything. The most flattering
    possible reading was the one that required no measurement, and it was the construction default.
    """
    def __init__(self, name: str, setpoint: float, ueg: Any):
        super().__init__(name, setpoint)
        self.pid = PIDController(setpoint=setpoint, kp=1.0, ki=0.1, kd=0.2)
        self.ueg = ueg
        self.state: Dict[str, Any] = {"current": None}

    async def sense(self) -> dict:
        _v = self.state["current"]
        return {"value": _v, "assessable": _v is not None,
                "basis": ("the last value regulate() was given"
                          if _v is not None else
                          "NOT ASSESSED: nothing has supplied a value to this controller, so it has no "
                          "reading. It is not at its setpoint — it is unmeasured")}

    async def regulate(self, current_value: float = None) -> dict:
        val = current_value if current_value is not None else self.state["current"]
        if not isinstance(val, (int, float)):
            #  A refusal is an outcome. Regulating towards a target from an unknown position would emit a
            #  correction computed from nothing, and the caller could not tell it apart from a real one.
            return {"correction": None,
                    "basis": ("NOT REGULATED: no current value was supplied and none has been recorded, "
                              "so there is no error term to act on")}
        error = self.setpoint - val
        correction = self.pid.compute(error)
        self.state["current"] = val + correction
        if self.ueg:
            await self.ueg.log_minimisation_event(f"{self.name}_regulation", {
                "correction": correction,
                "new_state": self.state["current"]
            })
        #  Same keys as the refusal above: a caller reading `basis` must not get undefined on the path
        #  that worked, or the only branch it can describe is the one that failed.
        return {"correction": correction,
                "basis": (f"PID correction from error {round(error, 4)} with gains "
                          f"kp={self.pid.kp} ki={self.pid.ki} kd={self.pid.kd}; {self.pid.gains_basis}")}
