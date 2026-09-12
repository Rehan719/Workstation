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
# Reconciled 2026-09-02 (W435). "Keep in lockstep" is no longer a comment asking nicely — the
# lockstep is ENFORCED by test_w435_plan_api_mirrors_the_doc_scorecard, which reads the doc's §7
# glyphs and fails on divergence. This mirror sat wrong for a day the moment the doc moved.
#
# Re-scored 2026-09-05 (W446) from VISION_FIDELITY_LEDGER.md v3 — a fresh six-region audit against a
# HEAD-booted backend, every finding refuted. Honestly DOWN: pillars 3, 5, 7, 8 and the Chief moved
# to "partial" because the audit found what a user meets first — the Living Organisation hub's
# DEFAULT tab is a detached Ollama roleplay outside the native fabric; every autonomy flag is OFF
# and stays OFF (genome generation 0, reflex arcs 0, immune defence uncalled); the GaaS gate covers
# 8 of 57 API modules and Change Control's tiers are prose; two biomimetic layers are vouched for by
# unwired files; the Chief is a values sentence plus recent instructions with 0 twin models. The
# doc's §7 rows carry the evidence; the delivery plan (FABLE_DELIVERY_PROMPT.md v11 rev 2) carries
# the work. These move back up only when the re-run audit says so.
_PILLARS: List[Dict[str, str]] = [
    # W434/W435/W446 — ◐: the journey runs end-to-end and discloses the floor (W436), but the
    # shipped VSB body presents floor scaffold as the enterprise's concept and the shared §10 gate
    # certifies it (ledger R2/R1); Mode 3 gates gate nothing; §4.6 Develop has no stage.
    {"pillar": "AI-mediated end-to-end Concept→Design→Delivery", "status": "partial"},
    {"pillar": "Generate a living Enterprise IDBO (VSB) for the user", "status": "strong"},
    # W446 — ◐: the full-hierarchy cascade is real, but the hub's default tab bypasses the fabric
    # (R3.0), review gates are advisory (R3.1), Board deliberation is API-only (R3.4).
    {"pillar": "VSB org (Board→AI CEO→C-Suite→CoE→BTO) curates work", "status": "partial"},
    # W446 — ◐ (R3.4/R3.8): founder_profile is a constant values string + the last five
    # instructions; /api/v1/twin/models holds 0 models; nothing invokes the Chief unprompted.
    {"pillar": "Chief = Owner's digital twin (apex, arms-length)", "status": "partial"},
    {"pillar": "Reconfigurable, combinable resource fabric — compositions run their REAL engines", "status": "strong"},
    # W446 — ◐ (R6.7/R4.6/R6.1/R6.5): autonomy flags default OFF and persist OFF; reflex arcs 0;
    # immune-reconfigure has no caller; the survival instinct keys off a non-depleting simulator.
    {"pillar": "One self-running, self-healing, self-improving organism", "status": "partial"},
    {"pillar": "Synthesis Lab — any/all content output types", "status": "partial"},
    # W446 — ◐ (R6.0/R3.2/R1.1/R1.3): GaaS gate on 8/57 modules; CCA tiers unenforced, no auth;
    # the Constitutional compliance row never reads the subject; a FAIL ships an unmarked export.
    {"pillar": "Constitutional governance throughout (gaas.v5 + UEG; governed economy)", "status": "partial"},
    # W446 — ◐ (R4.5/R4.6/R6.1): Cardiovascular = CPU-idle relabelled, Endocrine = an unimported
    # PID file (the W434 quality note vouching for them is itself the overclaim); reflex arcs
    # cannot fire; the §8→§12 survival instinct is a dead branch.
    {"pillar": "Biomimetic mediation (biology/biogeo-physical)", "status": "partial"},
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
        "Stream /establish through the full vsb/spawn cascade (SSE) (done, W255 — POST /api/v1/genesis/establish/stream)",
        "Absorb the v191 evolution fragment under the Sovereign Evolution Office (done, W261 — the /api/v191 mount stays as an unreached legacy namespace with no frontend caller; retire-or-keep is a scatter decision)",
    ],
    "long": [
        "Per-VSB living lifecycle — Board+Chief+economy+plan on every generated VSB (done, W248)",
        "Forge ⇄ Build-to-Order ⇄ Catalogue wired to the Resource Fabric (done, W246)",
        "Cross-VSB federation & marketplace (partial — in-instance contracts/transfers/marketplace live; cross-instance honestly simulated by Owner decision, vision §18-E)",
        "User isolation (the §17.5 invariant) on business routers (partial — open on the control perimeter: heartbeat, genome, organism-status, sovereign-evolution, board, change-control, business-plan, swarm; delivery plan P2.6)",
        "Digital-twin pre-validation in Change Control (HIGH/CRITICAL) (done, W253 — health-gate fallback when no twin model; P1.11)",
        "Persistence hardening (store_lock + atomic writes done across the money/UEG/registry stores; DB Owner-gated), GaaS YAML genome activation",
        "The whole-vision delivery plan — FABLE_DELIVERY_PROMPT.md v11 rev 2: P1 truth → P2 reach/disclosure → P3 capability → P4 Owner switches",
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
