"""
Shared helper: run a completion on Workstation's OWN native fabric and return the text plus
in-house provenance. Used by the Domain routers (Law/Science/Care/Education/Religion/Employment)
so every AI-mediated domain response demonstrably runs in-house (served_by) — same contract as
Forge/Genesis. In-house-first; never a dependency on an external provider.
"""
from __future__ import annotations

import time
from typing import Any, Dict, Tuple

from agentic_core.ai.gateway import gateway


async def ai_text(prompt: str, agent: str, timeout: float = 30.0,
                  owner_id: str | None = None, augment: bool = False) -> Tuple[str, Dict[str, Any]]:
    """Return (text, provenance) where provenance = {posture, served_by, is_external}.

    Every call is recorded into the operational-excellence learning loop (best-effort, non-critical)
    so rankings/summary reflect REAL platform AI usage — which OWNED resource served each domain tool,
    how often, how fast, in-house vs external — not just swarm runs.

    W332/W333 — Offering-1 output is a deliverable that the user SEES and SAVES, so recall injection
    (the cross-tenant leak) is defaulted OFF here (`augment=False`); when a caller opts into recall it
    is tenant-scoped by `owner_id`. Domain routers thread the authenticated user's id."""
    t0 = time.monotonic()
    res = await gateway.query_meta(prompt, agent=agent, timeout=timeout,
                                   owner_id=owner_id, augment=augment)
    output = res.get("output", "")
    served_by = res.get("served_by", "native")
    is_external = bool(res.get("is_external"))
    try:
        from agentic_core.api.operational_excellence import record_outcome
        record_outcome("ai_call", f"agent:{agent}", served_by=served_by, is_external=is_external,
                       duration_ms=int((time.monotonic() - t0) * 1000), success=bool(output))
    except Exception:
        pass
    provenance: Dict[str, Any] = {"posture": "in-house-first", "served_by": served_by,
                                  "is_external": is_external}
    # §10×§11 (W308) — Offering-1 GATED: every domain-tool / refine response passes the SAME living
    # QMS + compliance gate as the cascade and deliverables (assure_delivery). FLAG, never block:
    # the user always gets their output; the quality/compliance posture rides on the provenance the
    # UI already renders. Failures open traceable QMS defects (label = the serving agent).
    try:
        from agentic_core.vbs.quality import assure_delivery
        _qa = (await assure_delivery(output, None, label=f"tool:{agent}"))["quality"]
        provenance["quality_assurance"] = {
            "qms_gate_passed": _qa.get("qms_gate_passed"),
            "delivery_coverage": _qa.get("delivery_coverage"),
            "stub_found": _qa.get("stub_found"),
            "compliance_overall": (_qa.get("compliance") or {}).get("overall"),
            "quality_record_hash": _qa.get("quality_record_hash"),
        }
    except Exception as exc:   # the gate itself must never cost the user their output
        provenance["quality_assurance_error"] = str(exc)
    return output, provenance
