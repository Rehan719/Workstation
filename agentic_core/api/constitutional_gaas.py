"""
Constitutional GaaS API — v16-Omega governance engine HTTP surface.

Exposes the :mod:`agentic_core.gaas.v5` constitutional interception stack so any
client can route an action through the gate, inspect the self-tuning circuit
breaker, and audit the tamper-evident Unified Event Graph (UEG).

  GET  /api/v1/gaas/status         — engine status (breaker + UEG summary)
  POST /api/v1/gaas/intercept      — route an action through the constitutional gate
  GET  /api/v1/gaas/ueg/events     — recent UEG events (audit trail)
  GET  /api/v1/gaas/ueg/verify     — verify the UEG hash-chain integrity
  POST /api/v1/gaas/breaker/reset  — reset the node circuit breaker
"""
from __future__ import annotations

from typing import Any, Dict, Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from agentic_core.auth.core import auth_enabled, require_admin

from agentic_core.gaas.v5 import UnifiedConstitutionalInterceptorV16Omega, UEGLogger

router = APIRouter(prefix="/api/v1/gaas", tags=["constitutional-gaas"])

# A single sovereign-node interceptor backs the HTTP surface. The UEG persists to
# meta/ so the audit trail survives restarts.
_UEG = UEGLogger()
_INTERCEPTOR = UnifiedConstitutionalInterceptorV16Omega("sovereign-node", _UEG)


class InterceptRequest(BaseModel):
    action_type: str
    payload: Dict[str, Any] = {}
    requires_human: bool = False
    human_approved: bool = False
    # Optional text to run through the post-execution output gate. If omitted, a
    # synthesised acknowledgement is validated instead.
    proposed_output: Optional[str] = None


@router.get("/status")
async def gaas_status():
    """Live engine status: version, circuit-breaker state, and UEG summary."""
    return {
        "engine": "agentic_core.gaas.v5",
        "interceptor": "UnifiedConstitutionalInterceptorV16Omega",
        "node": _INTERCEPTOR.node_id,
        "circuit_breaker": _INTERCEPTOR.circuit_breaker.state(),
        # §10 (W494, FU-141) — this breaker belongs to the module-level "sovereign-node" interceptor,
        # which ONLY POST /api/v1/gaas/intercept drives. Every other governed path builds its own
        # interceptor per call (board.py:363 "board-node", economy.py:711 "economy-node",
        # forge.py "forge-node", and so on), each with its own breaker, and nothing aggregates them.
        # So a green NOMINAL here with error_rate 0.0 was read as "the live constitutional engine is
        # healthy" when it only ever said "one route's breaker has not tripped" — and that route is
        # rarely called, so the figure could not move.
        "circuit_breaker_node": _INTERCEPTOR.node_id,
        # W494 (refutation) - the first version said this route "and nothing else", which is itself a
        # claim the code does not support: the resource fabric's gaas_v5 requisition drives the same
        # module-level interceptor through /api/v1/resources/compose and /compositions/{cid}/run. A
        # scope that under-reports sends a reader looking in one place.
        "circuit_breaker_covers": ["POST /api/v1/gaas/intercept",
                                   "the resource fabric's gaas_v5 requisition "
                                   "(/api/v1/resources/compose, /compositions/{cid}/run)"],
        "circuit_breaker_scope": (
            f"the '{_INTERCEPTOR.node_id}' interceptor only, which is driven by POST "
            "/api/v1/gaas/intercept and by the resource fabric's gaas_v5 requisition. Every other "
            "governed path constructs its own "
            "interceptor per call with its own breaker (board-node, economy-node, forge-node and "
            "others); none of those is reflected here and no surface aggregates them. This is not a "
            "platform-wide constitutional health figure."),
        "ueg": _UEG.summary(),
        "articles_enforced": ["11.1 (UCI)", "7.3 (human escalation)", "5.2 (self-tuning breaker)"],
    }


@router.post("/intercept")
async def gaas_intercept(req: InterceptRequest):
    """
    Route an action through the constitutional gate. The pre-gate screens the
    intent, the action 'executes' (producing the proposed output), and the
    post-gate screens that output — all recorded to the UEG.
    """
    context: Dict[str, Any] = {
        "intent": req.action_type,
        "requires_human": req.requires_human,
        "human_approved": req.human_approved,
        **req.payload,
    }

    async def _action() -> str:
        if req.proposed_output is not None:
            return req.proposed_output
        return f"Action '{req.action_type}' executed under constitutional supervision."

    result = await _INTERCEPTOR.intercept(context, _action)

    # Fire a cognitive nervous signal so the organism registers the governance event.
    try:
        from agentic_core.organism.biobus import biobus
        biobus.fire_signal("cognitive", "gaas.intercept",
                           f"{req.action_type}:{result.status}", 0.6)
    except Exception:
        pass

    return result.to_dict()


@router.get("/ueg/events")
async def gaas_ueg_events(limit: int = 50):
    """Recent constitutional events from the Unified Event Graph (audit trail). W460 — each event carries
    `flag` (flagged | review | recorded) computed from what the event IS; the stored nodes are untouched."""
    from agentic_core.gaas.v5.ueg import classify_event
    recent = [{**n, "flag": classify_event(n.get("data") or {})} for n in _UEG.recent(limit)]
    return {"events": recent, "summary": _UEG.summary()}


@router.get("/ueg/verify")
async def gaas_ueg_verify():
    """Recompute the SHA3-512 hash-chain and confirm the audit log is untampered."""
    return _UEG.verify_chain()


@router.post("/breaker/reset")
async def gaas_breaker_reset(user: dict = Depends(require_admin)):
    """Manually reset the node's self-tuning circuit breaker (e.g. after remediation).

    W505 (FU-007) — an ADMIN act, and a recorded one. This clears a tripped constitutional breaker and had no
    dependency at all, so with auth on any unauthenticated caller could clear it; and it cleared the history
    silently, so the reason for the trip was gone with no trace of who cleared it. The dependency is inert in
    single-user mode (require_admin returns a synthetic admin when auth is off).
    """
    was = _INTERCEPTOR.circuit_breaker.state()
    _INTERCEPTOR.circuit_breaker.reset()
    _by = (user or {}).get("username") or "unknown"
    _recorded, _why = True, None
    try:
        _UEG.log({"type": "gaas.breaker_reset", "domain": was.get("domain"), "by": _by,
                  "by_verified": bool(auth_enabled()), "state_before_reset": was})
    except Exception as exc:
        _recorded, _why = False, f"{type(exc).__name__}: {exc}"
    return {"status": "reset", "circuit_breaker": _INTERCEPTOR.circuit_breaker.state(),
            "state_before_reset": was, "reset_by": _by,
            "reset_by_verified": bool(auth_enabled()),
            "recorded_in_ledger": _recorded,
            **({} if _recorded else {"not_recorded_because": _why})}
