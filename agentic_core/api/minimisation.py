"""The Biomimetic Minimisation Engine, reported — including the four terms that cannot be computed.

P3.17's bar: "every Ω term computes its named quantity or says it cannot; no second Landauer meter; the
transport router reports itself unavailable without a solver". This is the surface that says all three.

WHY A ROUTE AT ALL. Measured: nothing reached any of it. `optimal_transport.py` is a real Sinkhorn router
imported by no live module, the Ω-functional was in the archive, and the only way to discover that the
solver was missing was to call solve() and be thrown out of it by a RuntimeError. A component that can
report its own unavailability only by failing cannot be asked about itself.

WHAT THIS SURFACE WILL NOT DO:
  * It will not report J(π) from a partial sum. Four of the five Ω terms have no producer on this
    platform, and in a MINIMISATION an absent term defaulted to zero is the OPTIMUM — the archived
    version did exactly that, so the least-measured candidate always won. J is None unless every
    weighted term is assessable, and each refusal names the producer that would supply it.
  * It will not estimate a transport plan without a solver. An entropic optimal transport problem has no
    cheap approximation that deserves the same name.
  * It will not report a second Landauer meter. `entropy_export` is the one term with a real producer
    today, and that producer is the ONE thermodynamic ledger — this surface points at it and keeps no
    figure of its own.
"""
from __future__ import annotations

from typing import Any, Dict, Optional

from fastapi import APIRouter, Depends

from agentic_core.auth.core import get_current_user

router = APIRouter(prefix="/api/v1/minimisation", tags=["biomimetic-minimisation"])


@router.get("/status")
async def minimisation_status(user: dict | None = Depends(get_current_user)) -> Dict[str, Any]:
    """Every Ω term, what would produce it, and whether the transport solver is installed."""
    from agentic_core.biomimicry.minimisation.core.omega_functional import MinimisationObjective
    from agentic_core.biomimicry.minimisation.core.optimal_transport import OptimalTransportRouter

    _obj = MinimisationObjective()
    #  Evaluated with NO metrics on purpose: this is the platform's actual state, and the result is the
    #  honest report of it rather than a demonstration. If a term ever acquires a producer, it appears
    #  here without anyone editing this file.
    _omega = _obj.evaluate({}, {})
    _router = OptimalTransportRouter().availability()

    _tfel: Dict[str, Any]
    try:
        from core.transcendent_subsystems.tfel import ThermodynamicFreeEnergyLedger
        _led = ThermodynamicFreeEnergyLedger()
        _tfel = {"available": True, "temperature_kelvin": _led.temperature,
                 "joules_per_bit_floor": _led.E_min,
                 "basis": ("the one thermodynamic ledger. k_B*T*ln2 per bit is the Landauer FLOOR — the "
                           "minimum energy to erase a bit at this temperature — and not a measurement "
                           "of energy drawn. There is no second meter: this surface points at it and "
                           "keeps no figure of its own")}
    except Exception as e:                       # noqa: BLE001 — an absent ledger is reported
        _tfel = {"available": False, "temperature_kelvin": None, "joules_per_bit_floor": None,
                 "basis": f"NOT AVAILABLE: the thermodynamic ledger could not be imported ({e})"}

    return {
        "omega_functional": _omega,
        "transport_router": _router,
        "thermodynamic_ledger": _tfel,
        "terms_total": len(_obj.weights),
        "terms_assessable": len(_omega["assessable_terms"]),
        "basis": (
            f"{len(_omega['assessable_terms'])} of {len(_obj.weights)} Ω terms are assessable on this "
            f"platform today, so J(π) is {'reported' if _omega['J'] is not None else 'NOT REPORTED'}. "
            f"Each unassessable term names the producer that would supply it — a partial sum would be a "
            f"smaller number and an unknown cost, and in a minimisation that rewards incompleteness"),
    }
