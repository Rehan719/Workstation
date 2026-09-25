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
from agentic_core.config import atomic_write_json, data_path
from typing import Any, Dict, List

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from agentic_core.ai.gateway import gateway

router = APIRouter(prefix="/api/v1/business-plan", tags=["business-plan"])

_STORE = data_path("business_plans")


def _key(scope: str) -> str:
    """W488 (refutation) — the scope is a FILENAME, so it is reduced to one, not merely de-slashed.

    The old form replaced ':' and '/' and stopped there, which on Windows left a backslash live: a scope
    of '..\\..\\config' resolved outside business_plans/ entirely, so a read could serve another store's
    JSON as the Owner's plan and a write could overwrite it. Only letters, digits, '-' and '_' survive."""
    safe = "".join(c if (c.isalnum() or c in "-_") else "_" for c in str(scope or "")).strip("_")
    return safe[:120] or "workstation"


def _path(scope: str) -> Path:
    _STORE.mkdir(parents=True, exist_ok=True)
    return _STORE / f"{_key(scope)}.json"


def _load(scope: str) -> Dict[str, Any]:
    """W488 (sweep S3.10, C5) — THE OWNER'S PLAN IS READ WHOLE OR REFUSED, NEVER REPLACED.

    `_load` used to swallow JSONDecodeError and OSError and hand back a FRESH EMPTY plan. The page then
    showed no opening, '0 objectives' and 0%, and the very next write — an Add Objective, a +25%, an
    Owner edit, a Board directive — atomically overwrote the Owner's real plan with that empty one. A
    read that cannot be trusted must stop the write, not seed it. This is the same one strict read every
    other store in this repository uses since W472 (config.read_json_strict → StoreUnavailable), and the
    routes below answer 503 rather than serving or overwriting an emptiness they invented.
    """
    from agentic_core.config import read_json_strict
    return read_json_strict(_path(scope), lambda: _fresh(scope), expect=dict)


def _load_or_503(scope: str) -> Dict[str, Any]:
    """Every ROUTE reads through this: an unreadable plan is a 503 naming the file, never an empty plan
    served as the Owner's and never a write that replaces it."""
    from agentic_core.config import StoreUnavailable
    try:
        return _load(scope)
    except StoreUnavailable as e:
        raise HTTPException(status_code=503, detail=(
            f"{e} — the business plan was NOT read and nothing was written. Fix or restore the file; "
            f"it is never replaced with an empty plan."))


def _fresh(scope: str) -> Dict[str, Any]:
    return {"scope": scope, "owner": "Rehan",
            # Chief-owned opening sections (the founder's idea, framed by the digital-twin Chief)
            "executive_summary": "", "concept": "", "vision": "",
            "mission": "", "strategy": "", "aims": [], "objectives": [], "updated_at": None}


def parse_objective_lines(text: str, extra: Dict[str, Any] | None = None) -> List[Dict[str, Any]]:
    """Parse 'TITLE | KPI | TIMELINE | OWNER_ROLE' pipe-lines into living-plan objective dicts.
    Shared by the Chief's plan generation AND the Board's chief_instruct delegation (§5 apex
    closure): the same machine-readable objective format lands on the roadmap from either path.
    `extra` fields (e.g. directive_id) are stamped onto every parsed objective."""
    out: List[Dict[str, Any]] = []
    for line in (text or "").splitlines():
        if line.count("|") >= 3 and not line.strip().lower().startswith(("## ", "title")):
            parts = [p.strip() for p in line.split("|")]
            title = parts[0].lstrip("-•0123456789. ").strip()
            if not title:
                continue
            out.append({
                "id": f"obj-{uuid.uuid4().hex[:8]}", "title": title[:120],
                "kpi": parts[1][:120], "timeline": parts[2][:60],
                "owner_role": parts[3][:40] if len(parts) > 3 else "AI CEO",
                "progress_pct": 0, "status": "planned", "reviews": [],
                "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                **(extra or {}),
            })
    return out


def _save(plan: Dict[str, Any]) -> None:
    plan["updated_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    atomic_write_json(_path(plan["scope"]), plan)


async def _q(prompt: str, agent: str) -> str:
    try:
        return await gateway.query(prompt, agent=agent)
    except Exception as e:
        return f"[{agent} unavailable: {e}]"


def parse_chief_draft(draft: str) -> tuple[Dict[str, str], str]:
    """W471 — the Chief's '## Section' blocks as {field: text}, and the PREAMBLE (every line before the
    first heading — the native floor's provenance marker and role line). The old parser dropped the
    preamble, so the floor's own disclosure never reached the plan."""
    sec_map = {"executive summary": "executive_summary", "concept": "concept", "vision": "vision",
               "mission": "mission", "strategy": "strategy"}
    cur = None
    seen_heading = False
    buf: Dict[str, List[str]] = {}
    pre: List[str] = []
    for line in (draft or "").splitlines():
        s = line.strip()
        head = None
        if s.startswith("#"):
            head = s.lstrip("#").strip()
        elif s.startswith("**") and s.endswith("**") and len(s) > 4:
            head = s.strip("*").strip()
        if head is not None:
            cur = sec_map.get(head.split("(")[0].strip().lower())   # an unmapped heading (Objectives) is skipped
            seen_heading = True
            continue
        if not seen_heading:
            if s:
                pre.append(s)
            continue
        if cur and s and "|" not in s:
            buf.setdefault(cur, []).append(s)
    return {f: " ".join(ls).strip()[:1200] for f, ls in buf.items()}, " ".join(pre).strip()[:600]


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
    plan = _load_or_503(scope)
    plan["roadmap"] = _roadmap(plan)   # living, derived — integrated into the plan, not persisted
    return plan


@router.get("/roadmap")
async def get_roadmap(scope: str = "workstation"):
    """The Chief's living delivery roadmap for this scope (time-phased objectives + trajectory)."""
    return _roadmap(_load_or_503(scope))


@router.get("/list")
async def list_plans():
    _STORE.mkdir(parents=True, exist_ok=True)
    # W488 (refutation) — A PLAN THAT CANNOT BE READ IS LISTED AS UNREADABLE, NEVER DROPPED.
    # The refusal added above covers every scoped route; this one still did its own tolerant read inside
    # `except Exception: pass`, so a present-but-corrupt plan vanished from `plans` AND from `total` —
    # indistinguishable from never having existed, one function below a docstring promising otherwise.
    # A listing is a read-only surface, so it answers 200 with the row marked, and says how many rows
    # it could not read; the counts it reports are only over the plans it actually read.
    plans: List[Dict[str, Any]] = []
    unreadable: List[Dict[str, Any]] = []
    for p in sorted(_STORE.glob("*.json")):
        try:
            d = json.loads(p.read_text(encoding="utf-8"))
            if not isinstance(d, dict):
                raise ValueError(f"expected an object, got {type(d).__name__}")
            plans.append({"scope": d.get("scope"), "objectives": len(d.get("objectives", [])),
                          "updated_at": d.get("updated_at"), "readable": True})
        except Exception as e:
            row = {"scope": p.stem, "objectives": None, "updated_at": None, "readable": False,
                   "unreadable_reason": f"{type(e).__name__}: {e}",
                   "note": "this plan exists and could not be read whole; nothing was overwritten"}
            plans.append(row)
            unreadable.append(row)
    return {"plans": plans, "total": len(plans), "readable_total": len(plans) - len(unreadable),
            "unreadable_total": len(unreadable),
            "counts_cover": "the plans listed as readable only" if unreadable else "every plan listed"}


_OPENING_FIELDS = ("executive_summary", "concept", "vision", "mission", "strategy")
_PENDING_MARK = "content pending the owned model"      # W450's pending-body marker (genesis._PENDING_BODY)


def _is_unset(value: Any) -> bool:
    """A field with nothing in it, or W450's pending marker — both are 'not yet composed'."""
    return not str(value or "").strip() or str(value).strip().startswith(_PENDING_MARK)


def _pending_fields(plan: Dict[str, Any]) -> List[str]:
    """body_pending as the plan stands: the seeded pending list (Genesis names design/commercialisation/operations
    too) plus every opening field that is unset — minus any the owner or a model has since filled."""
    seeded = [f for f in ((plan.get("provenance") or {}).get("body_pending") or []) if isinstance(f, str)]
    out = [f for f in seeded if f not in _OPENING_FIELDS or _is_unset(plan.get(f))]
    out += [f for f in _OPENING_FIELDS if _is_unset(plan.get(f)) and f not in out]
    return out


class SetPlanRequest(BaseModel):
    scope: str = "workstation"
    owner: str = "Rehan"
    executive_summary: str = ""      # Chief-owned opening sections (the founder's idea, framed by the Chief)
    concept: str = ""
    vision: str = ""
    mission: str = ""
    strategy: str = ""
    aims: List[str] = []
    clear: List[str] = []            # W471 — fields the owner empties (a set of "" never cleared anything)


@router.post("/set")
async def set_plan(req: SetPlanRequest):
    """Chief/Board set the plan's constitutional + strategic layers — the owner-edit surface (W471: wired
    from BusinessPlan.tsx; an owner's edit is recorded per field and lifts the field out of 'pending')."""
    plan = _load_or_503(req.scope)
    plan.update({"owner": req.owner or plan.get("owner", "Rehan")})
    ts = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    edits = plan.setdefault("owner_edits", {})
    for f in _OPENING_FIELDS:
        v = (getattr(req, f) or "").strip()
        if v and v.lower().startswith(_PENDING_MARK):
            raise HTTPException(status_code=422, detail=f"{f}: the floor's pending marker is not an owner's edit")
        if f in req.clear:
            if plan.get(f):                          # clearing what was there is an edit; clearing nothing is not
                plan[f] = ""
                edits[f] = ts
        elif v and v != (plan.get(f) or ""):         # (refutation) only a CHANGED value is an owner's edit
            plan[f] = v
            edits[f] = ts
    if req.aims:
        plan["aims"] = req.aims
    prov = plan.get("provenance")
    if isinstance(prov, dict):
        prov["body_pending"] = _pending_fields(plan)
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
    plan = _load_or_503(req.scope)
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
    plan = _load_or_503(req.scope)
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


class OrchestrateRequest(BaseModel):
    scope: str = "workstation"


@router.post("/objective/{oid}/orchestrate")
async def orchestrate_objective(oid: str, req: OrchestrateRequest):
    """The Chief delivers an objective via the autonomous in-house workflow TREE — grounded in the VSB +
    plan, governed (VBS QMS/DCMS · validation · minimax · swarm consensus · biomimetic signal) and sealed
    into the UEG provenance chain. The run is recorded as an auditable review on the objective."""
    plan = _load_or_503(req.scope)
    obj = next((o for o in plan["objectives"] if o["id"] == oid), None)
    if not obj:
        raise HTTPException(status_code=404, detail=f"Objective {oid} not found in {req.scope}.")

    # W452 (P1.4) — when the scope is a VSB, its Mode 3 review gates are consulted BEFORE the tree
    # runs (outside the grounding try/except below, which swallows exceptions by design).
    try:
        from agentic_core.api.vsb import _load_vsb as _gate_load
        _gated_vsb = _gate_load(req.scope)
    except Exception:
        _gated_vsb = None
    if _gated_vsb:
        from agentic_core.api.vsb import _refuse_gated
        _refuse_gated(_gated_vsb, "orchestrate")

    # Ground the run in the live VSB entity (when the scope is a generated VSB) + the plan's strategy.
    grounding = ""
    try:
        from agentic_core.api.vsb import _load_vsb
        v = _load_vsb(req.scope)
        if v:
            grounding = (f"VSB: {v.get('name')} (domain {v.get('domain')}, stage {v.get('stage')}); "
                         f"mission: {str(v.get('challenge', ''))[:160]}. ")
    except Exception:
        pass
    goal = (f"Deliver this objective: {obj['title']}."
            + (f" KPI: {obj['kpi']}." if obj.get("kpi") else "")
            + (f" Timeline: {obj['timeline']}." if obj.get("timeline") else ""))
    context = grounding + (f"Plan mission: {str(plan.get('mission', ''))[:200]}. "
                           f"Strategy: {str(plan.get('strategy', ''))[:200]}.")

    from agentic_core.ai.native import orchestrator
    tree = await orchestrator.orchestrate_tree(goal, context=context)

    decision = (tree.get("decision") or {}).get("recommendation")
    consensus = (tree.get("consensus") or {}).get("choice")
    # W437: the signal payload's key is supra_threshold (the old `propagated` was deleted with the
    # fabricated latency it travelled with) — and a MISSING signal_response must record null, not a
    # confident False (a determination nothing computed)
    _signal = tree.get("signal_response") or {}
    supra = bool(_signal["supra_threshold"]) if "supra_threshold" in _signal else None

    # §5 loop closure (W266) — delivery MOVES the living plan: a GENUINELY governed successful run
    # (the real QMS gate passed) advances a 'planned' objective to 'in_progress'. Never auto-'done'
    # (completion stays an Owner decision); a failed/ungoverned run leaves the status untouched.
    qms_passed = (tree.get("governance") or {}).get("qms_passed") is True   # W449: None (not assessable) never advances
    status_advanced = False
    if qms_passed and obj.get("status") == "planned":
        obj["status"] = "in_progress"
        status_advanced = True

    review = {
        "at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "progress_pct": obj.get("progress_pct", 0), "status": obj.get("status", "in_progress"),
        "note": (f"Chief workflow-tree delivery — decision={decision}, consensus={consensus}, "
                 f"signal={'not computed' if supra is None else 'supra-threshold' if supra else 'sub-threshold'}, "
                 f"nodes={tree.get('node_count')}"),
        "orchestration": {
            "decision": decision, "consensus": consensus,
            "qms_passed": (tree.get("governance") or {}).get("qms_passed"),
            "signal_supra_threshold": supra, "node_count": tree.get("node_count"),
            "ueg_hash": tree.get("ueg_hash"),
        },
    }
    obj.setdefault("reviews", []).append(review)
    _save(plan)

    try:
        from agentic_core.organism.biobus import biobus
        biobus.fire_signal("cognitive", "business_plan.orchestrate",
                           f"{req.scope}: Chief delivered '{obj['title'][:40]}' via tree ({decision})", 0.7)
    except Exception:
        pass

    return {"objective_id": oid, "goal": goal, "grounded_in": req.scope,
            "status": obj.get("status"), "status_advanced": status_advanced,
            # W490 (sweep S1.4, C7) — this whitelist STRIPPED the per-node served_by trace the
            # orchestrator builds, so no surface could say that every node of the "Chief workflow-tree"
            # was composed by the deterministic floor: the page showed `final` as a delivered decision
            # with nothing to distinguish it from model reasoning. The trace travels now (without each
            # node's output, which would bloat the payload), and so does any_external.
            "tree": {"node_count": tree.get("node_count"), "decision": tree.get("decision"),
                     "consensus": tree.get("consensus"), "governance": tree.get("governance"),
                     "validation": tree.get("validation"), "signal_response": tree.get("signal_response"),
                     "ueg_hash": tree.get("ueg_hash"), "final": tree.get("final"),
                     "nodes": [{"id": n.get("id"), "role": n.get("role"),
                                "served_by": n.get("served_by"), "is_external": n.get("is_external")}
                               for n in (tree.get("nodes") or [])],
                     "any_external": tree.get("any_external")}}


class GenerateRequest(BaseModel):
    scope: str = "workstation"
    context: str = ""


@router.post("/generate")
async def generate_plan(req: GenerateRequest):
    """Chief-mediated AI generation/refresh of the living business plan from org state + vision."""
    plan = _load_or_503(req.scope)
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
        + "\nProduce these sections, each under its own '## ' heading:\n"
        "## Executive Summary (2-3 sentences)\n## Concept (2-3 sentences)\n## Vision (one line)\n"
        "## Mission (one line)\n## Strategy (3-4 sentences)\n"
        "## Objectives (4-6, each: TITLE | KPI | TIMELINE | OWNER_ROLE)"
    )
    # W471 (P1.14, ledger R3.3) — the Chief's draft carries its PROVENANCE. On the native floor the "draft"
    # is prompt echo that ignores the founder's words (the floor keyed on the prompt's preamble), so nothing
    # is written to the plan from it: the floor's output is kept as chief_draft with its marker, the fields
    # stay pending the owned model, and the answer says so. A model-served draft fills EMPTY fields only —
    # never an owner's words on a refresh — and its preamble is kept as provenance, not dropped.
    # W488 (refutation) — augment=False here too. This is the SAME Chief-of-the-Board twin the round
    # fixed in board.py, twenty lines below the strict read it added — and this one PERSISTS its output
    # into the Owner's living plan (fields + objectives). With recall injected, another request's
    # content could be written into the plan as the founder's own words. The apex reads the Owner's
    # words and nothing else, on every path that speaks for the Chief.
    try:
        meta = await gateway.query_meta(prompt, agent="business_plan_chief", augment=False)
    except Exception as e:
        meta = {"output": f"[business_plan_chief unavailable: {e}]", "served_by": "unavailable", "is_external": False}
    draft = str(meta.get("output") or "")
    sb = str(meta.get("served_by") or "native")
    sections, preamble = parse_chief_draft(draft)
    ts = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    written: List[str] = []
    added = 0
    if sb in ("native", "unavailable"):
        reason = ("structured floor — not model analysis; nothing was written to the plan (the fields stay "
                  "pending the owned model; the owner can set them)" if sb == "native"
                  else "the owned model was unavailable; nothing was written to the plan")
    else:
        for field, text in sections.items():
            if text and _is_unset(plan.get(field)):          # empty, or W450's pending marker — never an owner's words
                plan[field] = text
                written.append(field)
                (plan.get("owner_edits") or {}).pop(field, None)   # a model's text is not an owner's edit
        # Parse objectives from the draft (TITLE | KPI | TIMELINE | OWNER_ROLE lines) — shared helper
        # so the Board's chief_instruct delegation lands objectives the same way (§5 apex closure, W265).
        new_objs = parse_objective_lines(draft)
        plan["objectives"].extend(new_objs)
        added = len(new_objs)
        reason = "" if written or added else (
            "the owned model served a draft but nothing was written — no recognised section met a field still "
            "unset (edit or clear a field to let the model fill it)" if sections else
            "the owned model's draft carried no recognised '## Section' headings — nothing was written")
    plan["chief_draft"] = draft
    # (refutation) MERGE into the plan's provenance: Genesis' name_source and seeded pending list stay; the
    # opening's served_by describes who wrote what is on screen, so it moves only when this generation wrote
    prov = dict(plan.get("provenance") or {})
    prov["generation"] = {"served_by": sb, "any_external": bool(meta.get("is_external")), "generated_at": ts,
                          "preamble": preamble, "written": written, "objectives_added": added, "reason": reason}
    if written:
        prov["served_by"] = {sb: 1}
        prov["any_external"] = bool(meta.get("is_external"))
    prov["preamble"] = preamble                                # the floor's marker / the model's lead-in, kept
    prov["written"] = written
    prov["body_pending"] = _pending_fields(dict(plan, provenance=prov))
    plan["provenance"] = prov
    _save(plan)

    try:
        from agentic_core.organism.biobus import biobus
        biobus.fire_signal("cognitive", "business_plan.generate",
                           f"{req.scope}: +{added} objectives, {len(written)} field(s) written ({sb})", 0.7)
    except Exception:
        pass

    return {"scope": req.scope, "chief_draft": draft, "objectives_added": added, "written": written,
            "served_by": sb, "reason": reason, "provenance": plan["provenance"], "plan": plan}


@router.get("/progress")
async def progress(scope: str = "workstation"):
    plan = _load_or_503(scope)
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
