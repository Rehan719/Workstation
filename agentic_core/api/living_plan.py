"""
Living Plan API — the self-updating, current-state-aware spine of the Design &
Development Action Plan (docs/WORKSTATION_IDBO_LIVING_PLAN.md).

This makes the plan *living*: `/state` introspects the running organism for a
grounded, never-stale current-state snapshot; `/plan` exposes the vision pillars,
phases, and an adherence scorecard so the Owner (and any agent) can monitor
understanding, progress, and vision-alignment programmatically.

  GET  /api/v1/plan          — vision pillars, phases (immediate/short/long), adherence scorecard
  GET  /api/v1/plan/state    — grounded current-state snapshot (auto-introspected, live)
"""
from __future__ import annotations

import time
from typing import Any, Dict, List

from fastapi import APIRouter

router = APIRouter(prefix="/api/v1/plan", tags=["living-plan"])

_DOC = "docs/WORKSTATION_IDBO_LIVING_PLAN.md"

# Vision pillars + adherence (mirrors §7 of the living plan; the doc is source-of-truth,
# this exposes it queryably). status: strong | partial | not_yet
# Reconciled 2026-08-12 (W251) — keep in lockstep with the doc's §7 scorecard.
_PILLARS: List[Dict[str, str]] = [
    {"pillar": "AI-mediated end-to-end Concept→Design→Delivery", "status": "strong"},
    {"pillar": "Generate a living Enterprise IDBO (VSB) for the user", "status": "strong"},
    {"pillar": "VSB org (Board→AI CEO→C-Suite→CoE→BTO) curates work", "status": "strong"},
    {"pillar": "Chief = Owner's digital twin (apex, arms-length)", "status": "strong"},
    {"pillar": "Reconfigurable, combinable resource fabric — compositions run their REAL engines", "status": "strong"},
    {"pillar": "One self-running, self-healing, self-improving organism", "status": "strong"},
    {"pillar": "Synthesis Lab — any/all content output types", "status": "partial"},
    {"pillar": "Constitutional governance throughout (gaas.v5 + UEG; governed economy)", "status": "strong"},
    {"pillar": "Biomimetic mediation (biology/biogeo-physical)", "status": "strong"},
    {"pillar": "Foundational values (integrity, halal, stewardship)", "status": "strong"},
]

_PHASES: Dict[str, List[str]] = {
    "immediate": [
        "gaas.v5 constitutional engine (done)",
        "Genesis journey + /establish living VSB (done)",
        "Sovereign Evolution Office (done)",
        "Resource Fabric (done)",
        "Board of Directors — Chief = Owner digital twin (done)",
        "Living Plan + Plan API (done)",
    ],
    "short": [
        "Resource compositions executable — every composed resource runs its REAL engine (done, W199–W250)",
        "Synthesis Lab explicit multi-output selection — 15 output types (done)",
        "Scheduled autonomy — circadian heartbeat runs evolution + living-VSB economy (done; governed W249)",
        "Stream /establish through the full vsb/spawn cascade (SSE)",
        "Absorb the v191 evolution fragment under the Sovereign Evolution Office",
    ],
    "long": [
        "Per-VSB living lifecycle — Board+Chief+economy+plan on every generated VSB (done, W248)",
        "Forge ⇄ Build-to-Order ⇄ Catalogue wired to the Resource Fabric (done, W246)",
        "Cross-VSB federation & marketplace",
        "User isolation (the §17.5 invariant) on business routers",
        "Digital-twin pre-validation in Change Control (HIGH/CRITICAL)",
        "Persistence hardening (atomic JsonStore → DB), GaaS YAML genome activation",
    ],
}


@router.get("")
async def get_plan():
    strong = sum(1 for p in _PILLARS if p["status"] == "strong")
    return {
        "document": _DOC,
        "vision_pillars": _PILLARS,
        "adherence": {
            "strong": strong,
            "partial": sum(1 for p in _PILLARS if p["status"] == "partial"),
            "not_yet": sum(1 for p in _PILLARS if p["status"] == "not_yet"),
            "score": round(strong / len(_PILLARS), 2),
        },
        "phases": _PHASES,
        "governance_hierarchy": ["Owner", "Chief (Owner Digital Twin)", "Board of Directors",
                                 "AI CEO", "C-Suite", "CoE", "BTO", "Operational Delivery"],
        "note": "Source of truth is the markdown doc; GET /plan/state for live current-state.",
    }


@router.get("/state")
async def get_state():
    """Grounded, auto-introspected snapshot of the live organism — so the plan never silently rots."""
    state: Dict[str, Any] = {"reconciled_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}

    try:
        from agentic_core.app_mvp import app
        state["api_routes"] = len(app.routes)
    except Exception:
        pass
    try:
        from agentic_core.api.resource_fabric import _REGISTRY, _load_compositions
        state["resources"] = len(_REGISTRY)
        state["resource_compositions"] = len(_load_compositions())
    except Exception:
        pass
    try:
        from agentic_core.api.vsb import _list_vsbs
        vsbs = _list_vsbs()
        state["vsb_entities"] = len(vsbs)
        state["vsb_recent"] = [v.get("name") for v in vsbs[:5]]
    except Exception:
        pass
    try:
        from agentic_core.api.sovereign_evolution import _load_roadmap
        rm = _load_roadmap()
        state["last_evolution_cycle"] = rm.get("created_at")
        state["evolution_items_proceeding"] = rm.get("items_proceeding")
    except Exception:
        pass
    try:
        from agentic_core.api.board import _BOARD, _load as _board_load
        state["board_directors"] = len(_BOARD)
        state["board_directives"] = len(_board_load())
    except Exception:
        pass
    try:
        from agentic_core.organism.immune import immune
        imm = immune.status()
        state["organism_health"] = imm.get("health")
        state["threat_level"] = imm.get("threat_level")
    except Exception:
        pass

    return state
