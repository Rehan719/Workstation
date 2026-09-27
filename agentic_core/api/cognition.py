"""
Cognition & Alignment Integration — wires the knowledge system into the organism.

Connects the FOUR knowledge layers (Understanding · Plan · Memory · Code/Live-State)
to EVERY operational tier — Chief, Board, AI CEO, C-Suite, CoE, BTO/Build-to-Order,
Swarm Cascade, arms-length Change Control, Heartbeat, Sovereign Evolution,
Transformation — so the organism self-aligns: AI-mediated, evidence-based, autonomous,
continuous, governed by gaas.v5 and audited to the UEG.

  GET  /api/v1/cognition/knowledge   — the 4 knowledge layers as live data (any agent/tier reads this)
  GET  /api/v1/cognition/wiring      — the integration map: each tier + endpoint + live "connected" status
  POST /api/v1/cognition/align       — autonomous, evidence-based alignment: route each vision gap to the
                                       right tier (Board / Evolution / Change Control). Plan-only by default;
                                       set execute=true to act (AI; arms-length, paced).
"""
from __future__ import annotations

import time
from typing import Any, Dict, List, Set

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/api/v1/cognition", tags=["cognition-alignment"])


def _routes() -> Set[str]:
    try:
        from agentic_core.app_mvp import app
        return {getattr(r, "path", "") for r in app.routes}
    except Exception:
        return set()


def _has(routes: Set[str], prefix: str) -> bool:
    return any(p.startswith(prefix) for p in routes)


# The living tiers the knowledge system is wired into (each with its endpoint).
_TIERS = [
    {"tier": "Chief (the Owner's charter; twin model planned) + Board", "endpoint": "/api/v1/board", "role": "apex direction; represents the Owner"},
    {"tier": "AI CEO → C-Suite → CoE (swarm cascade)", "endpoint": "/api/v1/swarm", "role": "executes direction; org intelligence"},
    {"tier": "BTO / Build-to-Order / Catalogue", "endpoint": "/api/v1/catalog", "role": "production & delivery"},
    {"tier": "Arms-length Change Control Agency", "endpoint": "/api/v1/cca", "role": "governs material changes"},
    {"tier": "Sovereign Evolution Office", "endpoint": "/api/v1/sovereign-evolution", "role": "self-improvement curation"},
    {"tier": "Organism Heartbeat (continuous autonomy)", "endpoint": "/api/v1/heartbeat", "role": "the rhythm that runs it all"},
    {"tier": "Vision→Realisation→Transformation", "endpoint": "/api/v1/transformation", "role": "measures vision realisation"},
    {"tier": "Living Plan", "endpoint": "/api/v1/plan", "role": "vision↔state↔action bridge"},
    {"tier": "VSB Economy (metabolism)", "endpoint": "/api/v1/economy", "role": "value flows & charitable giving"},
    {"tier": "Resource Fabric", "endpoint": "/api/v1/resources", "role": "reconfigurable resources"},
    {"tier": "Genesis / VSB generation", "endpoint": "/api/v1/genesis", "role": "generates living Enterprise IDBOs"},
    {"tier": "gaas.v5 + UEG (constitutional)", "endpoint": "/api/v1/gaas", "role": "governance & tamper-evident audit"},
    {"tier": "Monitoring / introspection", "endpoint": "/api/v1/plan/state", "role": "live current-state evidence (scraping seam)"},
]

# Evidence-based routing: which tier owns the action for each vision-gap pillar.
_GAP_ROUTING: Dict[str, Dict[str, str]] = {
    "end_to_end":       {"tier": "Board", "endpoint": "/api/v1/board/directive", "action": "set strategic direction"},
    "generate_vsb":     {"tier": "Board", "endpoint": "/api/v1/board/directive", "action": "prioritise VSB generation"},
    "vsb_org":          {"tier": "Board", "endpoint": "/api/v1/board/directive", "action": "org direction"},
    "chief_twin":       {"tier": "Board", "endpoint": "/api/v1/board", "action": "governance"},
    "resource_fabric":  {"tier": "Sovereign Evolution", "endpoint": "/api/v1/sovereign-evolution/cycle", "action": "improve capability"},
    "self_running":     {"tier": "Heartbeat", "endpoint": "/api/v1/heartbeat/configure", "action": "tune autonomy"},
    "synthesis_lab":    {"tier": "Sovereign Evolution", "endpoint": "/api/v1/sovereign-evolution/cycle", "action": "build capability"},
    "governance":       {"tier": "Change Control", "endpoint": "/api/v1/cca/submit", "action": "governed change"},
    "biomimetic":       {"tier": "Sovereign Evolution", "endpoint": "/api/v1/sovereign-evolution/cycle", "action": "system improvement"},
    "economy":          {"tier": "Board", "endpoint": "/api/v1/board/directive", "action": "economic direction"},
    "living_alignment": {"tier": "Transformation", "endpoint": "/api/v1/transformation/tick", "action": "self-measure"},
}


@router.get("/knowledge")
async def knowledge_layers():
    """The four synchronised knowledge layers, served live for any agent/tier."""
    out: Dict[str, Any] = {
        "understanding": {"doc": "docs/WORKSTATION_IDBO_UNDERSTANDING.md",
                          "role": "the same-page artifact: who the Owner is, vision, what I believe you want, open questions"},
        "plan": {"doc": "docs/WORKSTATION_IDBO_LIVING_PLAN.md", "api": "/api/v1/plan",
                 "process": "docs/KNOWLEDGE_OPERATING_PROCESS.md"},
        "memory": {"location": "agent memory canon (MEMORY.md + project/feedback/reference notes)"},
        "code_live_state": {"api": "/api/v1/plan/state + /api/v1/transformation/realisation"},
    }
    try:
        from agentic_core.api.living_plan import _PILLARS
        out["plan"]["vision_pillars"] = [p["pillar"] for p in _PILLARS]
    except Exception:
        pass
    try:
        from agentic_core.api.transformation import _realise
        out["code_live_state"]["overall_realisation"] = _realise().get("overall_realisation")
    except Exception:
        pass
    return out


@router.get("/wiring")
async def wiring_map():
    """The integration map — how the knowledge system connects to every living tier."""
    # §7 (W494, FU-139) — "connected" is a MOUNTED-ROUTE check: _has() asks whether any registered
    # path starts with the tier's prefix. Every tier's router is imported at app start, so it cannot be
    # false while the app is running: the endpoint reported "13/13 connected · 100% coherence" and a
    # green tick per tier, which the page read as the knowledge system being wired into each tier.
    # It says what it tests now, and the figure that cannot fail is named as such rather than being
    # presented as a coherence measurement.
    routes = _routes()
    tiers = [{**t, "route_mounted": _has(routes, t["endpoint"]),
              # kept for readers that already index it, with the meaning stated beside it
              "connected": _has(routes, t["endpoint"]),
              "connected_basis": ("a route starting with this tier's prefix is mounted in this process; "
                                  "nothing here checks that the knowledge system reaches the tier")}
             for t in _TIERS]
    mounted = sum(1 for t in tiers if t["route_mounted"])
    return {
        "tiers": tiers,
        "connected": mounted,
        "routes_mounted": mounted,
        "total": len(tiers),
        "coherence": round(mounted / len(tiers), 3),
        "coherence_measured": False,
        "coherence_basis": (
            f"{mounted} of {len(tiers)} tiers have a route mounted under their prefix. This is a "
            "MOUNTED-ROUTE count, not a measurement of integration: every tier's router is imported at "
            "startup, so it cannot come out below 100% while the app answers at all. Nothing here "
            "exercises a tier or checks that knowledge reaches it."),
        "principle": ("Knowledge layers → Transformation (measures realisation) → routed to the right tier "
                      "(Board / Evolution / Change Control) → governed by gaas/UEG → continuous via the Heartbeat."),
    }


class AlignRequest(BaseModel):
    execute: bool = False    # plan-only by default; true = act (AI; arms-length, paced)


@router.post("/align")
async def align(req: AlignRequest):
    """
    Autonomous, evidence-based alignment: introspect vision realisation, and route each
    gap to the tier that owns it. Plan-only by default (cheap). With execute=true it acts.
    """
    try:
        from agentic_core.api.transformation import _realise
        r = _realise()
    except Exception as e:
        return {"error": f"realisation unavailable: {e}"}

    routed: List[Dict[str, Any]] = []
    for p in r["pillars"]:
        if p["status"] == "realised":
            continue
        route = _GAP_ROUTING.get(p["id"], {"tier": "Board", "endpoint": "/api/v1/board/directive", "action": "review"})
        missing = [c["label"] for c in p["evidence"] if not c["met"]]
        routed.append({"gap": p["pillar"], "realisation": p["realisation"],
                       "routed_to": route["tier"], "endpoint": route["endpoint"],
                       "action": route["action"], "missing": missing, "executed": False})

    executed = []
    if req.execute and routed:
        # Act on the single highest-priority gap (lowest realisation) to stay paced + cost-safe.
        target = min(routed, key=lambda x: x["realisation"])
        try:
            if "sovereign-evolution" in target["endpoint"]:
                from agentic_core.api.sovereign_evolution import run_cycle, CycleRequest
                res = await run_cycle(CycleRequest(focus=f"close gap: {target['gap']}"))
                executed.append({"gap": target["gap"], "tier": target["routed_to"], "ref": res.get("cycle_id")})
            elif "board" in target["endpoint"]:
                from agentic_core.api.board import board_directive, BoardDirective
                res = await board_directive(BoardDirective(topic=f"Close vision gap: {target['gap']}"))
                executed.append({"gap": target["gap"], "tier": target["routed_to"], "status": res.get("status")})
            target["executed"] = True
        except Exception as e:
            executed.append({"gap": target["gap"], "error": str(e)})

    # Constitutional audit
    try:
        from agentic_core.gaas.v5 import UEGLogger
        UEGLogger().log({"type": "cognition_align",
                                                "gaps": len(routed), "executed": len(executed),
                                                "overall_realisation": r["overall_realisation"]})
    except Exception:
        pass
    try:
        from agentic_core.organism.biobus import biobus
        biobus.fire_signal("cognitive", "cognition.align", f"{len(routed)} gaps routed", 0.7)
    except Exception:
        pass

    return {
        "overall_realisation": r["overall_realisation"],
        # §17 (W496, FU-111) - the page rendered "Overall realisation 97% ... (evidence-based)" from
        # this figure while the producer describes it as route-mount and non-empty-store coverage.
        "measure": r["measure"],
        "gaps_routed": routed,
        "executed": executed,
        "aligned_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "note": "Evidence-based routing of vision gaps to the living tiers. Set execute=true to act.",
    }
