"""The six biogeochemical cycles as a reported control surface (P3.19).

WHY THIS ROUTE EXISTS AT ALL: because nothing reached the six. Measured W543 — no live module imports any
of HydrologicManager, DataCarbonCycle, NitrogenFixationDaemon, MetabolicScheduler, PhosphorusMemoryManager
or SulfurErrorManager. The package LOOKS live because a sibling does the work:
agentic_core/biomimicry/cycles/utils.py exports `constitutional_guard`, which ten cognitive engines
import, so a reachability check that greps the package finds a crowd of importers and concludes the cycles
run. They do not. Meanwhile three outside specifications describe them as a running PID control layer
holding ±5% across six cycles, and `enriched_layers.geospheric_homeostasis` — which IS on the UCI
interception path — called itself "Six-cycle PID-controlled homeostasis" while delegating to a shim that
consults none of them.

WHAT THIS SURFACE WILL AND WILL NOT SAY:
  * A cycle bound to a figure this platform measures reports it WITH THE READER THAT PRODUCED IT, so the
    number can be checked against its source rather than taken on trust.
  * A cycle bound to nothing reports assessable:false and names the reader that would bind it. Three of
    six are in that state today and the route says so plainly rather than rounding them to a zero.
  * A SETPOINT IS AN ASPIRATION until something measures the variable (this item's body), so every
    setpoint is reported with setpoint_is_aspiration set from whether its cycle is actually bound.
  * A GAIN IS A DEFAULT until tuned and the record says so, so the gains travel with gains_tuned:false
    and the basis naming where the literals came from.
  * There is NO deviation and NO homeostatic verdict for an unassessable cycle. Not a null beside a
    number, not a zero: the keys are absent, because a deviation from an unmeasured variable is not a
    deviation and must not be available to a consumer that would render it.

IT OPENS NO STORE. Every figure comes from the module that owns it, through
agentic_core/biomimicry/cycles/bindings.py, which calls no data_path() and writes nothing.
"""
from __future__ import annotations

from typing import Any, Dict, Optional

from fastapi import APIRouter, Depends

from agentic_core.auth.core import get_current_user
from agentic_core.biomimicry.cycles import bindings

router = APIRouter(prefix="/api/v1/cycles", tags=["biogeochemical-cycles"])

#  The declared setpoints and gains, read from the cycle modules that carry them rather than retyped
#  here — a second copy of these literals is how this surface would come to disagree with the code it
#  describes. Each entry is (module, class) and the values are read live below.
_CYCLE_MODULES = {
    "water": ("agentic_core.biomimicry.cycles.water_cycle", "HydrologicManager"),
    "carbon": ("agentic_core.biomimicry.cycles.carbon_cycle", "DataCarbonCycle"),
    "nitrogen": ("agentic_core.biomimicry.cycles.nitrogen_cycle", "NitrogenFixationDaemon"),
    "oxygen": ("agentic_core.biomimicry.cycles.oxygen_cycle", "MetabolicScheduler"),
    "phosphorus": ("agentic_core.biomimicry.cycles.phosphorus_cycle", "PhosphorusMemoryManager"),
    "sulfur": ("agentic_core.biomimicry.cycles.sulfur_cycle", "SulfurErrorManager"),
}

_TOLERANCE_BASIS = ("the ±5% tolerance is DECLARED by the three outside specifications "
                    "(docs/BIOGEOCHEMICAL_AND_COMMS_REVIEW.md), not derived from this platform's data")


async def _declared(name: str) -> Dict[str, Any]:
    """The setpoint, tolerance and gains a cycle module declares — read, not retyped.

    Returns a three-state answer of its own: a cycle whose module cannot be constructed reports that
    rather than a set of plausible defaults, because defaults here would look exactly like a reading.
    """
    mod_name, cls_name = _CYCLE_MODULES[name]
    try:
        import importlib
        cls = getattr(importlib.import_module(mod_name), cls_name)
        obj = cls(None, None, None)
        pid = getattr(obj, "pid", None)
        #  THE CLASS'S OWN sense() TRAVELS WITH ITS DECLARATION, which is what makes the six cycles
        #  REACHED rather than merely described by a route that reads around them. Until this round each
        #  sense() returned its reservoir literal and a homeostatic verdict computed from it, and no live
        #  module called any of them — so the fabrication sat in code that nothing could reach and
        #  nothing could show. It now says NOT ASSESSED, on a surface, with the literal disclosed.
        _sense: Optional[Dict[str, Any]]
        try:
            import asyncio
            _s = getattr(obj, "sense", None)
            if asyncio.iscoroutinefunction(_s):
                _sense = await _s()
            else:
                #  A STATED ABSENCE, NOT A NULL. water_cycle.HydrologicManager is the odd one of the six:
                #  it does not extend GeosphericCycle, defines no sense(), and carries its OWN duplicate
                #  PIDController class rather than the shared one. A null here would read as "nothing to
                #  report" when the fact is that this cycle has no reading method at all.
                _sense = {"assessable": False, "homeostatic": None,
                          "basis": (f"NOT ASSESSED: {cls_name} defines no sense() and does not extend "
                                    f"GeosphericCycle, so it has no reading method. It also declares a "
                                    f"second PIDController of its own rather than the shared one")}
        except Exception as e:                   # noqa: BLE001
            _sense = {"assessable": False,
                      "basis": f"the cycle's own sense() raised {e.__class__.__name__}: {e}"}
        return {
            "declared_sense": _sense,
            "setpoint": getattr(obj, "setpoint", None) or getattr(pid, "setpoint", None),
            "tolerance": getattr(obj, "tolerance", None),
            "gains": ({"kp": pid.kp, "ki": pid.ki, "kd": pid.kd} if pid is not None else None),
            "gains_tuned": bool(getattr(pid, "gains_tuned", False)),
            "gains_basis": getattr(pid, "gains_basis",
                                   "this cycle's controller declares no provenance for its gains"),
            "declared_read_from": f"{mod_name}.{cls_name}",
        }
    except Exception as e:                       # noqa: BLE001 — an unreadable declaration is reported
        #  the same key set as the success branch above, so a reader never meets a missing field
        return {"declared_sense": None,
                "setpoint": None, "tolerance": None, "gains": None, "gains_tuned": False,
                "gains_basis": (f"NOT READ: {mod_name}.{cls_name} could not be constructed "
                                f"({e.__class__.__name__}: {e}), so its declared gains are unknown"),
                "declared_read_from": None}


@router.get("")
async def list_cycles(vsb_id: Optional[str] = None,
                      user: dict | None = Depends(get_current_user)) -> Dict[str, Any]:
    """Every cycle, what it is bound to, and what it refuses to claim."""
    bound = bindings.read_all(vsb_id)
    out = []
    for name, b in bound.items():
        d = await _declared(name)
        assessable = bool(b.get("assessable"))
        row: Dict[str, Any] = {
            "name": name,
            "subject": b.get("subject"),
            "assessable": assessable,
            "measured_from": b.get("measured_from"),
            "basis": b.get("basis"),
            **({"value": b["value"]} if "value" in b else {}),
            "setpoint": d["setpoint"],
            #  AN ASPIRATION FOR ALL SIX, AND THE REASON IS SHARPER THAN "NOTHING MEASURES IT". The first
            #  draft of this route set this flag from the bound flag and then computed a deviation for the
            #  three bound cycles. It produced a deviation of 11.0 for water: a liquidity of 900 virtual
            #  WST against a setpoint of 75.0 — and water_cycle.regulate_homeostasis(current_temp) shows
            #  what that 75.0 actually is, a TEMPERATURE. The value and the setpoint were in different
            #  units, so the arithmetic was real, both inputs were real, and the figure was meaningless.
            #  That is this item's own defect class one level further in, and it was committed inside the
            #  fix for it. NO SETPOINT IN THESE SIX MODULES DECLARES A UNIT, so none of them is comparable
            #  to the figure its cycle is now bound to, and every one of them stays an aspiration.
            "setpoint_is_aspiration": True,
            "setpoint_basis": (
                f"the setpoint {d['setpoint']} is a target this cycle's module declares as a bare number "
                f"with NO UNIT stated anywhere"
                + (f", and the figure this cycle is bound to is measured in a different quantity "
                   f"({b.get('basis', '')[:60]}...). Comparing them would be arithmetic over "
                   f"incommensurable units, so no deviation is reported"
                   if assessable else
                   ", and nothing measures the variable it names, so there is nothing to compare it to")),
            "tolerance": d["tolerance"],
            "tolerance_basis": _TOLERANCE_BASIS,
            "gains": d["gains"],
            "gains_tuned": d["gains_tuned"],
            "gains_basis": d["gains_basis"],
            "declared_read_from": d["declared_read_from"],
            #  the cycle class's own reading, now on a surface
            "declared_sense": d["declared_sense"],
        }
        #  NO DEVIATION KEY ON ANY CYCLE, AND NOT A NULL EITHER — the keys are absent. Two conditions
        #  must hold before a deviation means anything: the variable must be measured, and the setpoint
        #  must be in the same unit as the measurement. The first holds for three cycles; the second
        #  holds for none, because no setpoint in these modules states a unit at all. A null beside a
        #  setpoint invites `deviation ?? 0`; an absent key forces a consumer to read the basis.
        row["deviation_basis"] = (
            "NOT COMPUTED: a deviation needs the measurement and the setpoint in the SAME UNIT, and none "
            "of the six setpoints declares a unit. Binding a unit to each setpoint is the work that makes "
            "a deviation reportable — until then the figure would be arithmetically sound and meaningless")
        out.append(row)

    _bound_n = sum(1 for r in out if r["assessable"])
    return {
        "cycles": out,
        "bound": _bound_n,
        "total": len(out),
        "vsb_id": vsb_id,
        "coupling_matrix": None,
        "coupling_basis": (
            "NOT REPORTED: the archived orchestrator holds a 6x6 coupling matrix and a Lyapunov bound, "
            "and a coupling between two cycles is only meaningful once BOTH are measured. "
            f"{_bound_n} of {len(out)} are bound today, so publishing a coupling would describe a "
            "relation between figures that do not exist"),
        "basis": (
            f"{_bound_n} of {len(out)} cycles are bound to a figure this platform measures; the rest "
            f"report the reader that would bind them. No figure here is stored by this surface — each is "
            f"read from the module that owns it at request time, so there is no second copy to diverge"),
    }
