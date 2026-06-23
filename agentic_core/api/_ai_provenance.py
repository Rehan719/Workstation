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


async def ai_text(prompt: str, agent: str, timeout: float = 30.0) -> Tuple[str, Dict[str, Any]]:
    """Return (text, provenance) where provenance = {posture, served_by, is_external}.

    Every call is recorded into the operational-excellence learning loop (best-effort, non-critical)
    so rankings/summary reflect REAL platform AI usage — which OWNED resource served each domain tool,
    how often, how fast, in-house vs external — not just swarm runs."""
    t0 = time.monotonic()
    res = await gateway.query_meta(prompt, agent=agent, timeout=timeout)
    output = res.get("output", "")
    served_by = res.get("served_by", "native")
    is_external = bool(res.get("is_external"))
    try:
        from agentic_core.api.operational_excellence import record_outcome
        record_outcome("ai_call", f"agent:{agent}", served_by=served_by, is_external=is_external,
                       duration_ms=int((time.monotonic() - t0) * 1000), success=bool(output))
    except Exception:
        pass
    return output, {"posture": "in-house-first", "served_by": served_by, "is_external": is_external}
