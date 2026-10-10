"""
Living Vision → Realisation → Transformation engine.

This is the organ that holds, as ONE living picture: the Owner's **Vision**, its
**current realisation in the live current state** (computed from real evidence,
not asserted), and the **transformation plan** derived from the gap between them.

It is AI-mediated, dynamic, adaptive, self-improving, and continuously operating:
it deeply introspects every subsystem of Workstation IDBO, scores realisation per
vision pillar from live evidence, derives the next transformation actions, runs a
heartbeat (`/tick`) that fires nervous signals and can feed the Sovereign Evolution
Office, and exposes an AI-mediated narrative assessment.

  GET  /api/v1/transformation              — the unified living picture (vision + realisation + plan)
  GET  /api/v1/transformation/realisation  — per-pillar realisation, computed from live evidence
  POST /api/v1/transformation/assess       — AI-mediated narrative assessment + guidance
  POST /api/v1/transformation/tick         — one continuous heartbeat cycle (introspect → signal → feed)
"""
from __future__ import annotations

import time
from pathlib import Path
from agentic_core.config import data_path
from typing import Any, Callable, Dict, List, Optional, Set

from fastapi import APIRouter

from agentic_core.ai.gateway import gateway

router = APIRouter(prefix="/api/v1/transformation", tags=["vision-transformation"])


# ── deep introspection of the live organism ───────────────────────────────────
def _routes() -> Optional[Set[str]]:
    #  W613 (FU-504, M1 v8 R6.0) — the shared census: OpenAPI paths plus flat routes, and None (not an empty
    #  set) when it cannot be read, so an unreadable census is never reported as "not mounted".
    from agentic_core.route_inventory import mounted_paths
    return mounted_paths()[0]


def _has(routes: Optional[Set[str]], prefix: str) -> Optional[bool]:
    if routes is None:
        return None
    return any(p.startswith(prefix) for p in routes)


def _evidence_counts() -> Dict[str, Any]:
    d: Dict[str, Any] = {}
    try:
        from agentic_core.api.vsb import _list_vsbs
        d["vsbs"] = len(_list_vsbs())
    except Exception:
        d["vsbs"] = 0
    try:
        d["economy_ledgers"] = len(list(data_path("economy").glob("*_ledger.json")))
    except Exception:
        d["economy_ledgers"] = 0
    try:
        from agentic_core.api.resource_fabric import _REGISTRY, _load_compositions
        d["resources"] = len(_REGISTRY)
        d["compositions"] = len(_load_compositions())
    except Exception:
        d["resources"] = 0
        d["compositions"] = 0
    try:
        from agentic_core.api.sovereign_evolution import _load_roadmap
        d["last_evolution"] = _load_roadmap().get("created_at")
    except Exception:
        d["last_evolution"] = None
    try:
        from agentic_core.organism.immune import immune
        d["organism_health"] = immune.status().get("health")
        d["organism_health_basis"] = ("the immune system's health: AI-call failures and compliance regressions "
                                      "only - route 5xx failures are not tracked")   # W635 (FU-587)
    except Exception:
        d["organism_health"] = None
    return d


# ── the vision, mapped to LIVE evidence checks ────────────────────────────────
# Each pillar's realisation is computed from the fraction of its evidence checks met.
Check = Callable[[Set[str], Dict[str, Any]], bool]

_PILLARS: List[Dict[str, Any]] = [
    {"id": "end_to_end", "pillar": "AI-mediated end-to-end Concept→Design→Delivery", "evidence": [
        ("Genesis journey live", lambda r, d: _has(r, "/api/v1/genesis/journey")),
        ("Process-intelligence engines live", lambda r, d: _has(r, "/api/v1/intelligence")),
    ]},
    {"id": "generate_vsb", "pillar": "Generate a living Enterprise IDBO (VSB) for the user", "evidence": [
        ("Establish endpoint live", lambda r, d: _has(r, "/api/v1/genesis")),
        ("VSB entities exist", lambda r, d: d.get("vsbs", 0) > 0),
        ("VSB spawn pipeline live", lambda r, d: _has(r, "/api/v1/vsb")),
    ]},
    {"id": "vsb_org", "pillar": "VSB org curates work (Board→AI CEO→C-Suite→CoE→BTO)", "evidence": [
        ("Board of Directors live", lambda r, d: _has(r, "/api/v1/board")),
        ("Org swarm cascade live", lambda r, d: _has(r, "/api/v1/swarm")),
        ("Sovereign Evolution Office live", lambda r, d: _has(r, "/api/v1/sovereign-evolution")),
    ]},
    # W492 (refutation) - the pillar is the ROLE; the evidence below checks the Board is live, which is
    # not evidence of a trained twin model, so the pillar says which of the two it claims.
    {"id": "chief_twin",
     "pillar": ("Chief = the Owner's digital twin as a ROLE (apex, arms-length) — no twin model is "
                "trained"), "evidence": [
        ("Board / Chief live", lambda r, d: _has(r, "/api/v1/board")),
    ]},
    {"id": "resource_fabric", "pillar": "Reconfigurable, combinable resource fabric", "evidence": [
        ("Resource Fabric live", lambda r, d: _has(r, "/api/v1/resources")),
        ("Resources federated (≥10)", lambda r, d: d.get("resources", 0) >= 10),
    ]},
    {"id": "self_running", "pillar": "One self-running, self-healing, self-improving organism", "evidence": [
        ("Self-evolution live", lambda r, d: _has(r, "/api/v1/sovereign-evolution")),
        ("An evolution cycle has run", lambda r, d: bool(d.get("last_evolution"))),
        ("Continuous heartbeat (scheduler)", lambda r, d: _has(r, "/api/v1/heartbeat")),
    ]},
    {"id": "synthesis_lab", "pillar": "Synthesis Lab — any/all content output types", "evidence": [
        ("Synthesis Studio live", lambda r, d: _has(r, "/api/v1/studio")),
        ("Multi-type output pipelines (Forge)", lambda r, d: _has(r, "/api/v1/forge")),
    ]},
    {"id": "governance", "pillar": "Constitutional governance throughout (gaas.v5 + UEG)", "evidence": [
        ("gaas.v5 gate live", lambda r, d: _has(r, "/api/v1/gaas")),
    ]},
    {"id": "biomimetic", "pillar": "Biomimetic + biogeo-physical mediation", "evidence": [
        ("Economic metabolism live", lambda r, d: _has(r, "/api/v1/economy")),
    ]},
    {"id": "economy", "pillar": "VSB as hybrid Waqf/Trust autonomous economy", "evidence": [
        ("Economy engine live", lambda r, d: _has(r, "/api/v1/economy")),
        ("A VSB ledger exists", lambda r, d: d.get("economy_ledgers", 0) > 0),
    ]},
    {"id": "living_alignment", "pillar": "Living alignment: vision ↔ current state ↔ plan", "evidence": [
        ("Living Plan API live", lambda r, d: _has(r, "/api/v1/plan")),
        ("Transformation engine live", lambda r, d: _has(r, "/api/v1/transformation")),
    ]},
]

_SHORT_TERM = [
    "Make resource compositions + Genesis executable as live workflow pipelines",
    "Scheduled autonomy — a heartbeat that ticks the metabolism + evolution continuously",
    "Synthesis Lab explicit multi-output selection",
    "Unify legacy evolution fragments under the Sovereign Evolution Office",
]
_LONG_TERM = [
    "Per-VSB living business-plan lifecycle (Board → AI CEO appraisal loops)",
    "Forge ⇄ Build-to-Order ⇄ Catalogue wired to the Resource Fabric",
    "Cross-VSB federation & marketplace; real-money rails behind compliance",
]


#  W620 (FU-508, M2 v8 R6.4) — §17.5 INVARIANT 2, "a mandatory GaaS gate on every output", MEASURED rather than
#  assumed. No global gate exists: gating is per route, and the one HTTP middleware observes and does not gate.
#  The governance pillar used to be met by "the gaas router is mounted", which is true and says nothing about
#  whether outputs pass a gate. This counts the API modules whose code calls one of the gates, and the pillar
#  shows that figure and is not met until every module does. It is a CALL-SITE count, and says so: a module
#  that calls a gate somewhere is not proof that every one of its outputs passes it.
_GATE_CALLS = ("ai_text(", "query_meta(", "stream_meta(", ".intercept(", "_policy_verdict(",
               "ConstitutionalPolicyGate", "intent_gate_result(", "console_pre_gate(")


def _gaas_coverage() -> Dict[str, Any]:
    import pathlib as _pl
    api = _pl.Path(__file__).resolve().parent
    mods = sorted(p for p in api.glob("*.py") if not p.name.startswith("_"))
    gated = [p.stem for p in mods if any(c in p.read_text(encoding="utf-8", errors="replace") for c in _GATE_CALLS)]
    return {"gated_modules": len(gated), "api_modules": len(mods),
            "basis": (f"{len(gated)} of {len(mods)} API modules call a constitutional or output gate somewhere in "
                      f"their code (a call-site count: it does not prove every output of those modules passes it). "
                      f"There is NO global gate - the HTTP middleware observes and does not gate - so an output of "
                      f"the other {len(mods) - len(gated)} passes no GaaS gate. §17.5 invariant 2 is NOT held.")}


def _realise() -> Dict[str, Any]:
    from agentic_core.route_inventory import mounted_paths
    routes, census = mounted_paths()
    data = _evidence_counts()
    pillars = []
    total = 0.0
    for p in _PILLARS:
        checks = []
        for lbl, fn in p["evidence"]:
            _m = fn(routes, data)
            checks.append({"label": lbl, "met": None if _m is None else bool(_m)})
        if p["id"] == "governance":
            _gc = _gaas_coverage()
            checks.append({"label": (f"GaaS gate on EVERY output (§17.5 invariant 2): {_gc['gated_modules']} of "
                                     f"{_gc['api_modules']} API modules"),
                           "met": _gc["gated_modules"] == _gc["api_modules"], "basis": _gc["basis"]})
        _assessed = [c for c in checks if c["met"] is not None]
        met = sum(1 for c in _assessed if c["met"])
        #  a check whose census could not be read is NOT ASSESSED, and is left out of the fraction rather
        #  than counted as unmet
        frac = round(met / len(_assessed), 3) if _assessed else 0.0
        status = "realised" if frac >= 0.999 else ("partial" if frac > 0 else "seed")
        total += frac
        pillars.append({"id": p["id"], "pillar": p["pillar"], "realisation": frac,
                        "status": status, "evidence": checks,
                        #  W655 (ledger v15 R6.0) - WHAT WAS COUNTED, IN ITS OWN WORDS. `status` says "realised"
                        #  when every presence check passes; a mounted router is not a realised pillar. The
                        #  old field keeps its meaning for its readers; these say what the number is.
                        "checks_met": met, "checks_assessed": len(_assessed),
                        "checks_status": ("no check could be assessed" if not _assessed else
                                          "all checks present" if met == len(_assessed) else
                                          "some checks present" if met else "no check present"),
                        "coverage_basis": (f"{met} of {len(_assessed)} presence check(s) passed: whether a route "
                                           f"is mounted or a store has a record. This is coverage, not delivery; "
                                           f"it does not say the pillar is realised.")})
    overall = round(total / len(_PILLARS), 3) if _PILLARS else 0.0
    return {"overall_realisation": overall, "pillars": pillars, "evidence_counts": data,
            "route_census": census,
            # W475 (ledger v4 R6.0) — this figure is API SURFACE COVERAGE (routers mounted, stores non-empty), not
            # delivery; the delivery measure is the plan's item states at /api/v1/plan/state.
            "measure": "API surface coverage — pillar routers mounted and stores non-empty; not delivery "
                       "(the delivery measure is /api/v1/plan/state)",
            "reconciled_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}


def _transformation_plan(realisation: Dict[str, Any]) -> Dict[str, Any]:
    gaps = []
    for p in realisation["pillars"]:
        if p["status"] != "realised":
            missing = [c["label"] for c in p["evidence"] if not c["met"]]
            gaps.append({"pillar": p["pillar"], "realisation": p["realisation"], "missing": missing})
    return {
        "immediate_gaps": gaps,
        "short_term": _SHORT_TERM,
        "long_term": _LONG_TERM,
        "principle": "Transformation = close the gap between vision (the pillars) and live realisation.",
    }


@router.get("")
async def transformation_picture():
    """The unified living picture: vision + current realisation + transformation plan."""
    realisation = _realise()
    return {
        "vision_summary": ("AI-mediate working for any user in any realm/domain — Concept→Design→Delivery — "
                           "generating a bespoke living Enterprise IDBO (VSB); one self-running living organism."),
        "realisation": realisation,
        "transformation_plan": _transformation_plan(realisation),
        "source_of_truth": "docs/WORKSTATION_IDBO_UNDERSTANDING.md + WORKSTATION_IDBO_LIVING_PLAN.md",
    }


@router.get("/realisation")
async def realisation():
    return _realise()


@router.post("/assess")
async def assess():
    """AI-mediated narrative assessment of how faithfully the current state realises the vision."""
    r = _realise()
    summary = "\n".join(f"- {p['pillar']}: {int(p['realisation']*100)}% ({p['status']})" for p in r["pillars"])
    prompt = (
        "You are the Transformation Intelligence of the Workstation IDBO. Given the computed realisation of "
        "the Owner's vision below, assess honestly how faithfully the current state realises the vision and "
        "what to do next.\n\n"
        f"Overall realisation: {int(r['overall_realisation']*100)}%\n{summary}\n\n"
        "## Faithfulness Assessment\n## Biggest Gaps\n## Recommended Next Transformation Steps\n## Risks"
    )
    # W490 (sweep S6.7, C7) — `gateway.query` throws away served_by/is_external, so a panel headed
    # 'AI Assessment' could not say that the deterministic floor composed it from the prompt's own
    # headings. query_meta carries what the page needs; the assessment text is unchanged.
    _prov = {"served_by": None, "is_external": False}
    try:
        _meta = await gateway.query_meta(prompt, agent="transformation_assess", timeout=20,
                                         augment=False)   # stated, never inherited (W488's rule)
        narrative = _meta.get("output", "")
        _prov = {"served_by": _meta.get("served_by", "native"),
                 "is_external": bool(_meta.get("is_external"))}
    except Exception as e:
        narrative = f"[assessment unavailable: {e}]"
        _prov = {"served_by": None, "is_external": False, "failed": str(e)}
    # §17 (W496, FU-111) - `_realise()` names this figure "API surface coverage ... not delivery",
    # and every consumer dropped that field, so the number shipped as a realisation percentage. A
    # qualifier that does not travel with the figure is not a qualifier.
    return {"overall_realisation": r["overall_realisation"], "measure": r["measure"],
            "assessment": narrative, "ai_provenance": _prov}


@router.post("/tick")
async def tick():
    """One continuous heartbeat: introspect realisation, fire a nervous signal, and surface the next gap."""
    r = _realise()
    plan = _transformation_plan(r)
    try:
        from agentic_core.organism.biobus import biobus
        biobus.fire_signal("cognitive", "transformation.tick",
                           f"realisation {int(r['overall_realisation']*100)}%", 0.6)
    except Exception:
        pass
    next_gap = plan["immediate_gaps"][0]["pillar"] if plan["immediate_gaps"] else None
    return {
        "overall_realisation": r["overall_realisation"],
        "measure": r["measure"],           # W496 (FU-111) - the figure never ships without it
        "next_gap": next_gap,
        "open_immediate_gaps": len(plan["immediate_gaps"]),
        "ticked_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "note": "Continuous heartbeat; feed /api/v1/sovereign-evolution/cycle to act on gaps.",
    }
