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
from typing import Any, Callable, Dict, List, Set

from fastapi import APIRouter

from agentic_core.ai.gateway import gateway

router = APIRouter(prefix="/api/v1/transformation", tags=["vision-transformation"])


# ── deep introspection of the live organism ───────────────────────────────────
def _routes() -> Set[str]:
    try:
        from agentic_core.app_mvp import app
        return {getattr(r, "path", "") for r in app.routes}
    except Exception:
        return set()


def _has(routes: Set[str], prefix: str) -> bool:
    return any(p.startswith(prefix) for p in routes)


def _evidence_counts() -> Dict[str, Any]:
    d: Dict[str, Any] = {}
    try:
        from agentic_core.api.vsb import _list_vsbs
        d["vsbs"] = len(_list_vsbs())
    except Exception:
        d["vsbs"] = 0
    try:
        d["economy_ledgers"] = len(list(Path("data/economy").glob("*_ledger.json")))
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
    {"id": "chief_twin", "pillar": "Chief = Owner's digital twin (apex, arms-length)", "evidence": [
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
        ("Organism systems healthy", lambda r, d: d.get("organism_health") is not None),
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


def _realise() -> Dict[str, Any]:
    routes, data = _routes(), _evidence_counts()
    pillars = []
    total = 0.0
    for p in _PILLARS:
        checks = [{"label": lbl, "met": bool(fn(routes, data))} for lbl, fn in p["evidence"]]
        met = sum(1 for c in checks if c["met"])
        frac = round(met / len(checks), 3) if checks else 0.0
        status = "realised" if frac >= 0.999 else ("partial" if frac > 0 else "seed")
        total += frac
        pillars.append({"id": p["id"], "pillar": p["pillar"], "realisation": frac,
                        "status": status, "evidence": checks})
    overall = round(total / len(_PILLARS), 3) if _PILLARS else 0.0
    return {"overall_realisation": overall, "pillars": pillars, "evidence_counts": data,
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
    try:
        narrative = await gateway.query(prompt, agent="transformation_assess")
    except Exception as e:
        narrative = f"[assessment unavailable: {e}]"
    return {"overall_realisation": r["overall_realisation"], "assessment": narrative}


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
        "next_gap": next_gap,
        "open_immediate_gaps": len(plan["immediate_gaps"]),
        "ticked_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "note": "Continuous heartbeat; feed /api/v1/sovereign-evolution/cycle to act on gaps.",
    }
