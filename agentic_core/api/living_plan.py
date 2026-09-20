"""
Living Plan API — the self-updating, current-state-aware spine of the Design &
Development Action Plan (docs/WORKSTATION_IDBO_LIVING_PLAN.md).

This makes the plan *living*: `/state` introspects the running organism for a
grounded, never-stale current-state snapshot; `/plan` exposes the vision pillars,
phases, and an adherence scorecard so the Owner (and any agent) can monitor
understanding, progress, and vision-alignment programmatically.

  GET  /api/v1/plan          — vision pillars, phases (immediate/short/long), adherence scorecard
  GET  /api/v1/plan/state    — grounded current-state snapshot (auto-introspected, live)
  GET  /api/v1/plan/followups — the follow-up register: found-but-not-done work, scheduled in plan order (W462), and
                                the delivery plan's live state — PLAN NOW and the routes (W469)
"""
from __future__ import annotations

import json
import time
from pathlib import Path
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
        "Persistence hardening (partial — store_lock + atomic writes across the ledger/revenue/transfer/fund/venture/UEG/living-registry stores, the registry's last unserialised writers closed in W463, the owner-payments store and the service-contract store (claimed settles under a persisted transfer id) in W465; DB Owner-gated), GaaS YAML genome activation",
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
        "followups": _followup_summary(),
        "governance_hierarchy": ["Owner", "Chief (the Owner's charter; twin model planned)", "Board of Directors",
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


@router.get("/followups")
def get_followups():
    """W462 — the follow-up register: every task a round found and did not do, slotted into the delivery
    plan and scheduled in the plan's own item order (docs/FOLLOWUPS.json; rules in
    agentic_core/plan_followups.py). `integrity` is the same check the suite enforces — a problem is
    reported here rather than hidden, and a register this code cannot read or check is reported too,
    never a 500. A plain `def`: the check runs `git ls-files`, which must not block the event loop. The
    docs are not copied into the runtime image, so a deployed backend says the register is unavailable
    instead of inventing an empty one."""
    from agentic_core import plan_followups as fu
    base = {"register": "docs/FOLLOWUPS.json"}
    try:
        prompt = fu.read_doc(fu.PROMPT)
        living = fu.read_doc(fu.LIVING)
        raw = fu.REGISTER.read_bytes()
    except FileNotFoundError as exc:
        return {**base, "available": False,
                "reason": f"{Path(str(exc.filename)).name if exc.filename else 'a plan doc'} is not readable here "
                          "(missing) — the docs are not shipped in the runtime image"}
    except OSError as exc:
        return {**base, "available": False,
                "reason": f"{Path(str(exc.filename)).name if exc.filename else 'a plan doc'} could not be read "
                          f"({exc.strerror or type(exc).__name__}) — it may be locked by another program; the next "
                          "read tries again"}
    except UnicodeDecodeError as exc:
        return {**base, "available": False,
                "reason": f"a plan doc is not valid UTF-8 (byte {exc.start}) — re-save it as UTF-8"}
    try:
        reg = fu.parse_register(raw)
    except ValueError as exc:
        return {**base, "available": False,
                "reason": f"docs/FOLLOWUPS.json is not valid JSON ({type(exc).__name__}: {str(exc)[:120]})"}
    try:
        problems = fu.check(reg, prompt, living)
        if problems and all(p in fu.LOCKSTEP for p in problems):
            # the CLI writes the docs, then the register: a read that fell between them sees two moments.
            # Read once more before reporting drift that may only be a write in progress.
            try:
                prompt, living, reg = fu.read_doc(fu.PROMPT), fu.read_doc(fu.LIVING), fu.parse_register(fu.REGISTER.read_bytes())
            except OSError as exc:
                return {**base, "available": False,
                        "reason": f"{Path(str(exc.filename)).name if exc.filename else 'a plan doc'} could not be "
                                  f"read ({exc.strerror or type(exc).__name__}) — the next read tries again"}
            problems = fu.check(reg, prompt, living)
        # W469 — the delivery plan's live state, derived on every call from the plan's items and the register
        # W486 — the PACE, derived on every call from the register's own record of which round closed
        # each row and which round found it. The Owner asked to be able to see where this is going
        # without asking; a forecast that cannot be justified reports itself not assessable and says why.
        try:
            _forecast = fu.forecast(reg, prompt)
        except Exception as _fe:
            _forecast = {"assessable": False,
                         "not_assessable_because": f"the forecast raised {type(_fe).__name__}"}
        return {**base, "available": True, **fu.schedule(reg, prompt), "plan": fu.plan_now(reg, prompt),
                "forecast": _forecast,
                "routes": fu._routes(reg), "integrity": {"ok": not problems, "problems": problems}}
    except Exception as exc:   # a defect in the checker itself is still reported, never a 500
        return {**base, "available": False,
                "reason": f"the follow-up register could not be checked ({type(exc).__name__}: {str(exc)[:120]})"}


def _followup_summary() -> Dict[str, Any]:
    # GET /api/v1/plan must never fail because of the register — it only carries the counts
    try:
        from agentic_core import plan_followups as fu
        reg, prompt = fu.load(fu.REGISTER), fu.read_doc(fu.PROMPT)
        s = fu.schedule(reg, prompt)
        p = fu.plan_now(reg, prompt)
        try:
            f = fu.forecast(reg, prompt)
            _pace = {"rows_per_round": f["rate_used"]["closed_per_round"],
                     "rounds_projected_all": f["all_rows_rounds_projected"],
                     "rounds_projected_next": (f["next_item"] or {}).get("rounds_projected"),
                     "assessable": f["assessable"]}
        except Exception:
            _pace = {"assessable": False}
        return {**s["counts"], "next_plan_item": s["next_plan_item"],
                "plan_items_done": p["done"], "plan_items_total": p["total"],
                "pace": _pace, "api": "/api/v1/plan/followups"}
    except Exception as exc:
        return {"available": False, "reason": type(exc).__name__, "api": "/api/v1/plan/followups"}
