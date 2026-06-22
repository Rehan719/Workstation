"""
Shared helper: run a completion on Workstation's OWN native fabric and return the text plus
in-house provenance. Used by the Domain routers (Law/Science/Care/Education/Religion/Employment)
so every AI-mediated domain response demonstrably runs in-house (served_by) — same contract as
Forge/Genesis. In-house-first; never a dependency on an external provider.
"""
from __future__ import annotations

from typing import Any, Dict, Tuple

from agentic_core.ai.gateway import gateway


async def ai_text(prompt: str, agent: str, timeout: float = 30.0) -> Tuple[str, Dict[str, Any]]:
    """Return (text, provenance) where provenance = {posture, served_by, is_external}."""
    res = await gateway.query_meta(prompt, agent=agent, timeout=timeout)
    return res.get("output", ""), {
        "posture": "in-house-first",
        "served_by": res.get("served_by", "native"),
        "is_external": bool(res.get("is_external")),
    }
