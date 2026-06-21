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

from fastapi import APIRouter
from pydantic import BaseModel

from agentic_core.gaas.v5 import UnifiedConstitutionalInterceptorV16Omega, UEGLogger

router = APIRouter(prefix="/api/v1/gaas", tags=["constitutional-gaas"])

# A single sovereign-node interceptor backs the HTTP surface. The UEG persists to
# meta/ so the audit trail survives restarts.
_UEG = UEGLogger("meta/gaas_v5_ueg.json")
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
    """Recent constitutional events from the Unified Event Graph (audit trail)."""
    return {"events": _UEG.recent(limit), "summary": _UEG.summary()}


@router.get("/ueg/verify")
async def gaas_ueg_verify():
    """Recompute the SHA3-512 hash-chain and confirm the audit log is untampered."""
    return _UEG.verify_chain()


@router.post("/breaker/reset")
async def gaas_breaker_reset():
    """Manually reset the node's self-tuning circuit breaker (e.g. after remediation)."""
    _INTERCEPTOR.circuit_breaker.reset()
    return {"status": "reset", "circuit_breaker": _INTERCEPTOR.circuit_breaker.state()}
