"""
Living Business-Plan management — for Workstation IDBO and every generated VSB.

The Chief (the Owner's digital twin) and the Board own a LIVING business plan:
mission · vision · strategy · aims · objectives (each with KPI, timeline, owner-role,
progress, reviews). It is set, reviewed, and AI-generated (Chief-mediated), with the
Owner retaining control/governance/oversight. Scoped to "workstation" (the top-level
IDBO) or "vsb:{id}" (a generated VSB) — so users can do the same for their own entity.

  GET  /api/v1/business-plan?scope=workstation        — the living plan
  POST /api/v1/business-plan/set                       — set mission/vision/strategy/aims
  POST /api/v1/business-plan/objective                 — add a timelined, KPI'd objective
  POST /api/v1/business-plan/objective/{oid}/review    — review an objective's progress
  POST /api/v1/business-plan/generate                  — Chief-mediated AI plan generation/refresh
  GET  /api/v1/business-plan/progress?scope=...         — progress summary
  GET  /api/v1/business-plan/list                       — all plans
"""
from __future__ import annotations

import json
import time
import uuid
from pathlib import Path
from typing import Any, Dict, List

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from agentic_core.ai.gateway import gateway

router = APIRouter(prefix="/api/v1/business-plan", tags=["business-plan"])

_STORE = Path("data/business_plans")


def _key(scope: str) -> str:
    return scope.replace(":", "_").replace("/", "_") or "workstation"


def _path(scope: str) -> Path:
    _STORE.mkdir(parents=True, exist_ok=True)
    return _STORE / f"{_key(scope)}.json"


def _load(scope: str) -> Dict[str, Any]:
    p = _path(scope)
    if p.exists():
        try:
            return json.loads(p.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            pass
    return {"scope": scope, "owner": "Rehan", "mission": "", "vision": "", "strategy": "",
            "aims": [], "objectives": [], "updated_at": None}


def _save(plan: Dict[str, Any]) -> None:
    plan["updated_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    _path(plan["scope"]).write_text(json.dumps(plan, indent=2), encoding="utf-8")


async def _q(prompt: str, agent: str) -> str:
    try:
        return await gateway.query(prompt, agent=agent)
    except Exception as e:
        return f"[{agent} unavailable: {e}]"


def _roadmap(plan: Dict[str, Any]) -> Dict[str, Any]:
    """LIVING roadmap — derived from the plan's objectives (the Chief delivers Aims/Mission/Objectives
    via Strategy AND a living Roadmap). Time-phases the objectives, computes per-phase + overall
    progress, the current phase and next milestone. Not persisted — recomputed each read so it stays
    live as objectives progress. Honest: built only from real objectives, never invented."""
    objs = plan.get("objectives", []) or []
    phases: Dict[str, list] = {}
    order: List[str] = []
    for o in objs:
        tl = (str(o.get("timeline") or "").strip() or "Unscheduled")
        if tl not in phases:
            phases[tl] = []
            order.append(tl)
        phases[tl].append(o)
    phase_list = []
    for tl in order:
        items = phases[tl]
        prog = round(sum(int(i.get("progress_pct") or 0) for i in items) / len(items)) if items else 0
        complete = bool(items) and all((int(i.get("progress_pct") or 0) >= 100) or i.get("status") == "done" for i in items)
        phase_list.append({
            "timeline": tl,
            "progress_pct": prog,
            "complete": complete,
            "count": len(items),
            "objectives": [{"id": i.get("id"), "title": i.get("title"), "progress_pct": i.get("progress_pct", 0),
                            "status": i.get("status"), "kpi": i.get("kpi"), "owner_role": i.get("owner_role")} for i in items],
        })
    overall = round(sum(int(o.get("progress_pct") or 0) for o in objs) / len(objs)) if objs else 0
    current = next((p for p in phase_list if not p["complete"]), None)
    next_milestone = None
    if current:
        nm = next((o for o in current["objectives"] if int(o.get("progress_pct") or 0) < 100), None)
        if nm:
            next_milestone = {"phase": current["timeline"], "title": nm["title"], "progress_pct": nm.get("progress_pct", 0)}
    return {
        "living": True,
        "phases": phase_list,
        "phase_count": len(phase_list),
        "objective_count": len(objs),
        "overall_progress_pct": overall,
        "current_phase": current["timeline"] if current else None,
        "next_milestone": next_milestone,
        "note": "Living roadmap derived from the plan's objectives — it updates as objectives progress.",
    }


@router.get("")
async def get_plan(scope: str = "workstation"):
    plan = _load(scope)
    plan["roadmap"] = _roadmap(plan)   # living, derived — integrated into the plan, not persisted
    return plan


@router.get("/roadmap")
async def get_roadmap(scope: str = "workstation"):
    """The Chief's living delivery roadmap for this scope (time-phased objectives + trajectory)."""
    return _roadmap(_load(scope))


@router.get("/list")
async def list_plans():
    _STORE.mkdir(parents=True, exist_ok=True)
    plans = []
    for p in sorted(_STORE.glob("*.json")):
        try:
            d = json.loads(p.read_text(encoding="utf-8"))
            plans.append({"scope": d.get("scope"), "objectives": len(d.get("objectives", [])),
                          "updated_at": d.get("updated_at")})
        except Exception:
            pass
    return {"plans": plans, "total": len(plans)}


class SetPlanRequest(BaseModel):
    scope: str = "workstation"
    owner: str = "Rehan"
    mission: str = ""
    vision: str = ""
    strategy: str = ""
    aims: List[str] = []


@router.post("/set")
async def set_plan(req: SetPlanRequest):
    """Chief/Board set the plan's constitutional + strategic layers."""
    plan = _load(req.scope)
    plan.update({"owner": req.owner or plan.get("owner", "Rehan")})
    for f in ("mission", "vision", "strategy"):
        v = getattr(req, f)
        if v:
            plan[f] = v
    if req.aims:
        plan["aims"] = req.aims
    _save(plan)
    return plan


class ObjectiveRequest(BaseModel):
    scope: str = "workstation"
    title: str
    kpi: str = ""
    timeline: str = ""               # e.g. "Q3 2026", "30 days"
    owner_role: str = "AI CEO"       # delegated tier


@router.post("/objective")
async def add_objective(req: ObjectiveRequest):
    plan = _load(req.scope)
    obj = {
        "id": f"obj-{uuid.uuid4().hex[:8]}",
        "title": req.title, "kpi": req.kpi, "timeline": req.timeline,
        "owner_role": req.owner_role, "progress_pct": 0, "status": "planned",
        "reviews": [], "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    plan["objectives"].append(obj)
    _save(plan)
    return obj


class ReviewRequest(BaseModel):
    scope: str = "workstation"
    progress_pct: int = 0
    note: str = ""
    status: str = "in_progress"      # planned | in_progress | done | blocked


@router.post("/objective/{oid}/review")
async def review_objective(oid: str, req: ReviewRequest):
    plan = _load(req.scope)
    for obj in plan["objectives"]:
        if obj["id"] == oid:
            obj["progress_pct"] = max(0, min(100, req.progress_pct))
            obj["status"] = req.status
            obj["reviews"].append({"at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                                   "progress_pct": obj["progress_pct"], "note": req.note,
                                   "status": req.status})
            _save(plan)
            return obj
    raise HTTPException(status_code=404, detail=f"Objective {oid} not found in {req.scope}.")


class GenerateRequest(BaseModel):
    scope: str = "workstation"
    context: str = ""


@router.post("/generate")
async def generate_plan(req: GenerateRequest):
    """Chief-mediated AI generation/refresh of the living business plan from org state + vision."""
    plan = _load(req.scope)
    # Ground in the live vision realisation where available.
    realisation = None
    try:
        from agentic_core.api.transformation import _realise
        realisation = _realise().get("overall_realisation")
    except Exception:
        pass
    prompt = (
        "You are the Chief of the Board (the Owner's digital twin) drafting/refreshing the LIVING "
        f"business plan for scope '{req.scope}'.\n\n"
        f"Owner vision: AI-mediate working for any user — Concept→Design→Delivery — generating living VSB IDBO "
        f"entities; one self-running living organism.\n"
        + (f"Current vision realisation: {int(realisation*100)}%\n" if realisation is not None else "")
        + (f"Existing strategy: {plan.get('strategy','')[:300]}\n" if plan.get("strategy") else "")
        + (f"Owner context: {req.context}\n" if req.context else "")
        + "\nProduce:\n## Mission (one line)\n## Strategy (3-4 sentences)\n"
        "## Objectives (4-6, each: TITLE | KPI | TIMELINE | OWNER_ROLE)"
    )
    draft = await _q(prompt, "business_plan_chief")

    # Parse objectives from the draft (TITLE | KPI | TIMELINE | OWNER_ROLE lines).
    added = 0
    for line in draft.splitlines():
        if line.count("|") >= 3 and not line.strip().lower().startswith(("## ", "title")):
            parts = [p.strip() for p in line.split("|")]
            title = parts[0].lstrip("-•0123456789. ").strip()
            if not title:
                continue
            plan["objectives"].append({
                "id": f"obj-{uuid.uuid4().hex[:8]}", "title": title[:120],
                "kpi": parts[1][:120], "timeline": parts[2][:60],
                "owner_role": parts[3][:40] if len(parts) > 3 else "AI CEO",
                "progress_pct": 0, "status": "planned", "reviews": [],
                "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            })
            added += 1
    plan["chief_draft"] = draft
    if not plan.get("vision"):
        plan["vision"] = "AI-mediated working that generates living VSB IDBO entities for every user."
    _save(plan)

    try:
        from agentic_core.organism.biobus import biobus
        biobus.fire_signal("cognitive", "business_plan.generate", f"{req.scope}: +{added} objectives", 0.7)
    except Exception:
        pass

    return {"scope": req.scope, "chief_draft": draft, "objectives_added": added, "plan": plan}


@router.get("/progress")
async def progress(scope: str = "workstation"):
    plan = _load(scope)
    objs = plan["objectives"]
    if not objs:
        return {"scope": scope, "objectives": 0, "overall_progress": 0, "by_status": {}}
    by_status: Dict[str, int] = {}
    for o in objs:
        by_status[o["status"]] = by_status.get(o["status"], 0) + 1
    overall = round(sum(o.get("progress_pct", 0) for o in objs) / len(objs), 1)
    return {"scope": scope, "objectives": len(objs), "overall_progress": overall,
            "by_status": by_status, "owner": plan.get("owner"),
            "objectives_detail": [{"id": o["id"], "title": o["title"], "kpi": o["kpi"],
                                   "timeline": o["timeline"], "owner_role": o["owner_role"],
                                   "progress_pct": o["progress_pct"], "status": o["status"]} for o in objs]}
