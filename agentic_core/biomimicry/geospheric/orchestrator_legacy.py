import logging
from typing import Dict, Any, Optional
from agentic_core.ueg.logger import VSBUEGLogger

logger = logging.getLogger(__name__)

#  W543 — ONE SOURCE FOR THE TOLERANCE, used by the comparison AND by the sentence that reports it. It was
#  typed twice as a literal 0.05, once in the test and once in the message, so the two agreed only by
#  coincidence and a change to the comparison would have left the basis quietly describing the old bound.
#  AND ITS PROVENANCE IS PART OF IT: 0.05 is the ±5% the three outside specifications assert, not a figure
#  this platform derived or tuned. Per P3.19's body a setpoint is an aspiration until something measures
#  the variable, so this is recorded as declared, never as validated.
_TOLERANCE = 0.05
_TOLERANCE_BASIS = ("0.05 is the ±5% tolerance asserted by the three outside specifications "
                    "(docs/BIOGEOCHEMICAL_AND_COMMS_REVIEW.md); it is DECLARED, not derived from this "
                    "platform's data and not tuned against it")

class GeosphericHomeostaticOrchestrator:
    """
    Legacy Orchestrator shim for v∞-FINAL compatibility.
    """
    def __init__(self, ueg_logger: Optional[Any] = None):
        self.ueg = ueg_logger or VSBUEGLogger()

    async def step(self, inputs: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Report whether a drift figure was supplied and what it says — and nothing beyond that.

        W543 — WHAT THIS IS, MEASURED. It touches none of the six biogeochemical cycles: no live file
        imports any of them, and this shim is what `enriched_layers.geospheric_homeostasis` actually calls
        on the UCI interception path. Three things were wrong and all three favoured clearing:

        (a) `self.psi_score = 0.95` was a literal set in __init__ and returned from every step, and its
            one consumer logs it into the UEG for every intercepted action. So the immutable ledger
            carried a homeostasis figure nothing had computed, for every action the platform took.
        (b) `inputs.get("drift", 0) > 0.05` made a MISSING drift figure indistinguishable from a measured
            drift of zero, and the caller passes `context.get("geospheric", {})` — which is empty on every
            real call. So the gate returned NOMINAL always, and a gate that cannot do anything but clear
            is not a gate. This is the same default-to-approval shape P3.14 removed from the clearance
            chain, surviving one layer out.
        (c) The docstring said homeostasis was MAINTAINED. Nothing here maintains anything; it compares a
            number it is handed, and when it is handed none it now says so.
        """
        _drift = inputs.get("drift")
        if not isinstance(_drift, (int, float)):
            status = "NOT_ASSESSED"
            _basis = ("no drift figure was supplied, so homeostasis was NOT ASSESSED. This is not a pass: "
                      "an unmeasured cycle is neither within tolerance nor outside it, and the six "
                      "biogeochemical cycles are bound to no measured flow on this path at all")
        elif _drift > _TOLERANCE:
            status = "CONSTITUTIONAL_VIOLATION"
            _basis = (f"the supplied drift {_drift} is above the tolerance {_TOLERANCE} "
                      f"({_TOLERANCE_BASIS})")
        else:
            status = "NOMINAL"
            _basis = (f"the supplied drift {_drift} is at or below the tolerance {_TOLERANCE} "
                      f"({_TOLERANCE_BASIS})")

        result = {
            "status": status,
            #  THREE-STATE, and the consumer was changed in this same commit: it read this key with a
            #  default of 1.0, so simply deleting the fabricated 0.95 would have made the ledger record a
            #  PERFECT psi instead of a merely invented one.
            "psi_score": None,
            "psi_basis": ("NOT COMPUTED: no Ψ is computed anywhere on this path. The figure that stood "
                          "here was a literal assigned once and returned unchanged"),
            "status_basis": _basis,
            "cycles_consulted": [],
            "message": "Homeostasis step completed"
        }

        if self.ueg:
            await self.ueg.log_minimisation_event("geospheric_step", result)

        return result
