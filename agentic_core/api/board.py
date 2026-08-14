"""
Board of Directors — the apex governance tier of the Workstation IDBO / VSB.

Sits ABOVE the AI CEO (honouring the Arms-Length Agency invariant: the AI CEO
cannot instruct the board — direction flows down, not up). The board is led by
the **Chief** — a digital twin of the Owner — who represents the Owner faithfully
in their presence and absence, with diligence, honesty, loyalty, determination
and perfectionism. The Chief leads/appraises/develops a swarm of specialist
Directors who together own the Business plan, strategy, aims, mission and
objectives, and delegate a timelined/resourced/scheduled living action plan to
the AI CEO (→ C-Suite → CoE → BTO → operational delivery).

Every VSB IDBO entity generated for a user receives its own Board + a Chief that
is the digital twin of *that* VSB's owner.

  GET  /api/v1/board/status           — board composition, hierarchy, owner it represents
  GET  /api/v1/board/charter          — the board charter + arms-length governance model
  POST /api/v1/board/chief/instruct   — Owner instructs their Chief twin → board directive → AI CEO action plan
  POST /api/v1/board/directive        — the board issues a directive on a topic (directors weigh in)
"""
from __future__ import annotations

import json
import time
import uuid
from pathlib import Path
from agentic_core.config import data_path
from typing import Any, Dict, List, Optional

from fastapi import APIRouter
from pydantic import BaseModel

from agentic_core.ai.gateway import gateway

router = APIRouter(prefix="/api/v1/board", tags=["board-of-directors"])

_STORE = data_path("board_directives.json")

# The Owner this top-level board represents. (Per-VSB boards carry their own owner.)
_OWNER = {
    "name": "Rehan",
    "role": "Founder / Owner / Curator",
    "vision_summary": (
        "Workstation IDBO AI-mediates working for any user in any realm/domain — taking a "
        "challenge end-to-end (Concept → Design → Delivery) and generating a bespoke, living "
        "Enterprise IDBO (a VSB) that commercialises the user's solution. One self-running, "
        "self-healing, self-improving living organism."
    ),
    "fidelity_charter": (
        "Represent the Owner precisely, effectively, efficiently, systematically and punctually — "
        "reflecting their exact wishes and instructions, perfectly understood and remembered, with "
        "due diligence, honesty, sincerity, loyalty, determination, resilience and perfectionism."
    ),
}

# The Board roster. The Chief is the Owner's digital twin; directors own areas of direction.
_BOARD: List[Dict[str, str]] = [
    {"id": "chief", "title": "Chief of the Board (Owner's Digital Twin)",
     "mandate": "Represent the Owner; set direction; lead/appraise/develop the board; delegate to the AI CEO."},
    {"id": "dir_strategy", "title": "Director of Strategy & Vision",
     "mandate": "Business plan, strategy, aims, mission, objectives — coherence with the Owner's vision."},
    {"id": "dir_technology", "title": "Director of Technology & Architecture",
     "mandate": "Technical direction, architecture integrity, build quality, scalability."},
    {"id": "dir_governance", "title": "Director of Governance & Compliance",
     "mandate": "Constitutional alignment, gaas.v5 gate, risk, change control, audit integrity."},
    {"id": "dir_biomimetic", "title": "Director of Biomimetic Systems",
     "mandate": "Highest authority to monitor/change/control all VSB living processes (immune/nervous/genome/evolution)."},
    {"id": "dir_operations", "title": "Director of Operations & Delivery",
     "mandate": "BTO, Build-to-Order, facilities management, operational delivery to timeline."},
    {"id": "dir_finance", "title": "Director of Finance & Capital",
     "mandate": "Capital allocation, unit economics, commercial sustainability."},
    {"id": "dir_evolution", "title": "Director of Evolution & Learning",
     "mandate": "Continual self-improvement; ties the Sovereign Evolution Office to board direction."},
]


def _load() -> List[Dict[str, Any]]:
    if _STORE.exists():
        try:
            return json.loads(_STORE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return []
    return []


def _save(rows: List[Dict[str, Any]]) -> None:
    from agentic_core.config import atomic_write_json
    atomic_write_json(_STORE, rows)


async def _q(prompt: str, agent: str, provenance: Dict[str, Any] | None = None) -> str:
    """§6 (W270) — the APEX tier runs on the same in-house-first fabric as every lower tier:
    query_meta with owned-resource provenance recorded per call (the Board was previously the only
    AI-driven governance tier without served_by/any_external)."""
    _t0 = time.time()
    try:
        res = await gateway.query_meta(prompt, agent=agent)
        if provenance is not None:
            sb = res.get("served_by", "native")
            provenance["served_by"][sb] = provenance["served_by"].get(sb, 0) + 1
            provenance["any_external"] = provenance["any_external"] or bool(res.get("is_external"))
        # §5×§6 (W275) — the APEX accrues real operational rows like every lower tier (it was the
        # only AI-driven tier invisible to the learning loop and the measured-outcomes blocks).
        try:
            from agentic_core.api.operational_excellence import record_outcome
            record_outcome("ai_call", f"agent:{agent}", served_by=res.get("served_by", "native"),
                           is_external=bool(res.get("is_external")),
                           duration_ms=int((time.time() - _t0) * 1000),
                           success=bool((res.get("output") or "").strip()))
        except Exception:
            pass
        return res.get("output", "")
    except Exception as e:
        try:
            from agentic_core.api.operational_excellence import record_outcome
            record_outcome("ai_call", f"agent:{agent}", served_by="none", is_external=False,
                           duration_ms=int((time.time() - _t0) * 1000), success=False)
        except Exception:
            pass
        return f"[{agent} unavailable: {e}]"


def _live_intelligence(scope: str) -> str:
    """LIVE intelligence for the Chief's directive (W270): the scoped plan's real progress, the
    recent operational success rate, and the prior directives — so the apex instructs from today's
    measured state, not just the static charter. Every figure read from the system that measured it."""
    lines: List[str] = []
    try:
        from agentic_core.api.business_plan import _load as _bp_load
        objs = (_bp_load(scope) or {}).get("objectives", [])
        if objs:
            by = {}
            for o in objs:
                by[o.get("status", "?")] = by.get(o.get("status", "?"), 0) + 1
            lines.append(f"- Living plan ({scope}): {len(objs)} objectives — " +
                         ", ".join(f"{k}: {v}" for k, v in sorted(by.items())))
    except Exception:
        pass
    try:
        from agentic_core.api.operational_excellence import _load as _ops_load
        rows = _ops_load()[-50:]
        if rows:
            ok = sum(1 for r in rows if r.get("success"))
            lines.append(f"- Recent operations: {len(rows)} runs, success rate {round(ok / len(rows), 2)}")
    except Exception:
        pass
    try:
        prior = _load()[-2:]
        for p in prior:
            lines.append(f"- Prior directive {p.get('directive_id', p.get('topic', '?'))}: "
                         f"{str(p.get('instruction') or p.get('topic') or '')[:100]}")
    except Exception:
        pass
    if not lines:
        return ""
    return "\n\nLIVE INTELLIGENCE (today's measured state — ground your directive in it):\n" + "\n".join(lines)


def board_for_owner(owner_name: str, vision_summary: str = "") -> Dict[str, Any]:
    """Compose a Board (with a Chief = digital twin of the given owner) for a VSB entity."""
    return {
        "owner": owner_name,
        "chief": {
            "title": f"Chief of the Board — Digital Twin of {owner_name}",
            "fidelity_charter": _OWNER["fidelity_charter"],
        },
        "directors": [d for d in _BOARD if d["id"] != "chief"],
        "governance": "arms-length: AI CEO cannot instruct the board; board directs the AI CEO",
        "vision_summary": vision_summary or _OWNER["vision_summary"],
    }


@router.get("/status")
async def board_status():
    snapshot: Dict[str, Any] = {}
    try:
        from agentic_core.organism.immune import immune
        snapshot["organism_health"] = immune.status().get("health")
    except Exception:
        pass
    return {
        "board": "Workstation IDBO Board of Directors",
        "represents_owner": _OWNER["name"],
        "hierarchy": ["Owner", "Chief (Owner Digital Twin)", "Board of Directors",
                      "AI CEO", "C-Suite", "CoE", "BTO", "Operational Delivery"],
        "chief": _BOARD[0],
        "directors": [d for d in _BOARD if d["id"] != "chief"],
        "live": snapshot,
        "recent_directives": _load()[-5:],
    }


@router.get("/charter")
async def board_charter():
    return {
        "owner": _OWNER,
        "board": _BOARD,
        "arms_length_agency": (
            "The AI CEO and below cannot instruct the board or mutate the genome directly. "
            "Direction flows Owner → Chief → Board → AI CEO. The board can monitor, change, "
            "update, control and impact all VSB living processes (highest authority)."
        ),
        "applies_to": "The Workstation IDBO and every VSB IDBO entity it generates.",
    }


class ChiefInstruction(BaseModel):
    instruction: str
    owner: str = "Rehan"
    cascade_to_ceo: bool = True
    scope: str = "workstation"   # which living business plan receives the objectives (e.g. a vsb_id)


@router.post("/chief/instruct")
async def chief_instruct(req: ChiefInstruction):
    """
    The Owner instructs their Chief digital twin. The Chief interprets the instruction
    faithfully (representing the Owner), issues a board-level directive, and delegates a
    timelined/resourced action plan to the AI CEO.
    """
    directive_id = f"dir-{uuid.uuid4().hex[:8]}"
    provenance: Dict[str, Any] = {"posture": "in-house-first", "served_by": {}, "any_external": False}

    # 1. The Chief (Owner's digital twin) interprets and represents the Owner faithfully — grounded
    #    in LIVE intelligence (plan progress · operations · prior directives), not just the charter.
    chief_prompt = (
        f"You are the Chief of the Board — the digital twin of {req.owner}, the Owner/Founder of the "
        f"Workstation IDBO. {_OWNER['fidelity_charter']}\n\n"
        f"The Owner's vision: {_OWNER['vision_summary']}"
        f"{_live_intelligence(req.scope)}\n\n"
        f"The Owner's instruction:\n\"{req.instruction}\"\n\n"
        "Acting AS the Owner, produce a board-level directive that precisely realises their intent:\n"
        "## Owner Intent (restated faithfully, what they truly want)\n"
        "## Board Directive (the decision the board issues)\n"
        "## Director Assignments (which Director owns which part)\n"
        "## Success Criteria (how we know the Owner's wish is fulfilled)"
    )

    # §11 (W270) — the APEX direction runs under the same gaas.v5 constitutional gate as every lower
    # tier (a gate failure logs a LOUD UEG bypass event, never silent — the W249/W261 pattern).
    async def _directive_action() -> str:
        return await _q(chief_prompt, "board_chief", provenance)
    try:
        from agentic_core.gaas.v5 import UnifiedConstitutionalInterceptorV16Omega, UEGLogger
        _gov = UnifiedConstitutionalInterceptorV16Omega("board-node", UEGLogger())
        _res = await _gov.intercept({"intent": "board_chief_instruct", "owner": req.owner,
                                     "scope": req.scope}, _directive_action)
        directive = _res.output if isinstance(_res.output, str) else await _directive_action()
        governance = {"status": _res.status, "checkpoint": _res.checkpoint_id}
    except Exception as _e:
        directive = await _directive_action()
        try:
            from agentic_core.gaas.v5 import UEGLogger
            UEGLogger().log({"type": "board.governance_bypass", "directive_id": directive_id,
                             "error": str(_e)[:200],
                             "note": "gaas.v5 gate unavailable — apex directive ran ungated (logged loudly)."})
        except Exception:
            pass
        governance = {"status": "ungated_bypass_logged", "error": str(_e)[:160]}

    # 2. Delegate to the AI CEO as a timelined, resourced, scheduled action plan.
    action_plan = ""
    if req.cascade_to_ceo:
        ceo_prompt = (
            "You are the AI CEO receiving a directive from the Board of Directors. Break it into an "
            "executable, timelined, resourced action plan integrated with the VSB living systems and "
            "agent swarm.\n\n"
            f"Board directive:\n{directive[:1200]}\n\n"
            "## Strategic Objectives (one per line, EXACTLY formatted: TITLE | KPI | TIMELINE | OWNER_ROLE)\n"
            "## Action Plan (numbered tasks, each with owner-role, resource, and timeline)\n"
            "## Delegation (C-Suite → CoE → BTO assignments)\n"
            "## KPIs & Review Cadence"
        )
        action_plan = await _q(ceo_prompt, "board_ceo_delegate", provenance)

    # §5 apex closure (W265) — the delegation LANDS: parsed objectives (TITLE|KPI|TIMELINE|OWNER_ROLE)
    # are appended to the scoped LIVING business plan, tagged with this directive. When the serving
    # model yields no machine-readable lines (e.g. the deterministic native floor), the Owner's
    # instruction itself becomes ONE objective — the apex direction never again evaporates into prose.
    objectives_added = 0
    if req.cascade_to_ceo:
        try:
            from agentic_core.api import business_plan as bp_mod
            new_objs = bp_mod.parse_objective_lines(action_plan, extra={"directive_id": directive_id})
            if not new_objs:
                new_objs = bp_mod.parse_objective_lines(
                    f"{req.instruction[:110]} | (KPI to be set by the Board) | next review | AI CEO",
                    extra={"directive_id": directive_id, "source": "chief_instruct_fallback"})
            plan = bp_mod._load(req.scope)
            plan.setdefault("objectives", []).extend(new_objs)
            bp_mod._save(plan)
            objectives_added = len(new_objs)
        except Exception:
            objectives_added = 0   # board direction must never fail on plan I/O

    record = {
        "directive_id": directive_id,
        "owner": req.owner,
        "instruction": req.instruction,
        "chief_directive": directive,
        "ceo_action_plan": action_plan,
        "business_plan_scope": req.scope,
        "objectives_added": objectives_added,
        "ai_provenance": provenance,     # §6 — which OWNED resource served the apex (W270)
        "governance": governance,        # §11 — the gaas.v5 gate verdict over the apex direction
        "delegation_chain": ["Chief", "Board", "AI CEO", "C-Suite", "CoE", "BTO"],
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    rows = _load()
    rows.append(record)
    _save(rows)

    # §6 (W270) — seal the apex direction into the tamper-evident UEG ledger.
    try:
        from agentic_core.gaas.v5 import UEGLogger
        UEGLogger().log({"type": "board.chief_instruct", "directive_id": directive_id,
                         "owner": req.owner, "scope": req.scope,
                         "objectives_added": objectives_added,
                         "served_by": provenance["served_by"],
                         "any_external": provenance["any_external"],
                         "governance": governance.get("status")})
    except Exception:
        pass

    try:
        from agentic_core.organism.biobus import biobus
        biobus.fire_signal("cognitive", "board.chief_instruct",
                           f"{req.owner}: {req.instruction[:60]}", 0.85)
    except Exception:
        pass

    return record


class BoardDirective(BaseModel):
    topic: str
    domain: str = "enterprise"


def _director_grounding(did: str) -> str:
    """§5 (W279) — LIVE readings of the systems each director OWNS, so a director's input is
    grounded in the real state of their mandate, not invented. Best-effort per system; a system
    that cannot be read is reported 'unavailable' — never fabricated."""
    try:
        if did == "dir_strategy":
            from agentic_core.api.business_plan import _load as _bp
            objs = (_bp("workstation") or {}).get("objectives", [])
            by = {}
            for o in objs:
                by[o.get("status", "?")] = by.get(o.get("status", "?"), 0) + 1
            return f"living plan objectives by status: {by or 'none yet'}"
        if did == "dir_technology":
            from agentic_core.api.resource_fabric import _BY_ID
            from agentic_core.api.operational_excellence import model_health
            return (f"fabric catalogue: {len(_BY_ID)} resources; "
                    f"measured model resources: {len(model_health())}")
        if did == "dir_governance":
            from agentic_core.gaas.v5 import UEGLogger
            g = UEGLogger()._read()
            return f"UEG audit chain: {len(g.get('nodes', []))} sealed events, root {str(g.get('root_hash'))[:12]}…"
        if did == "dir_biomimetic":
            from agentic_core.organism.biobus import biobus
            ctx = biobus.organism_context()
            return (f"immune threat {(ctx.get('immune') or {}).get('threat_level')}; "
                    f"circadian {(ctx.get('circadian') or {}).get('cycle')}; "
                    f"ATP {(ctx.get('metabolic') or {}).get('atp_ratio')}")
        if did == "dir_operations":
            from agentic_core.config import data_path, load_json_tolerant
            runs = load_json_tolerant(data_path("org_cascade_runs.json"), []) or []
            last = runs[-1] if runs else {}
            return (f"org cascade runs: {len(runs)}; last quality: "
                    f"qms={((last.get('quality') or {}).get('qms_gate_passed'))} "
                    f"coverage={((last.get('quality') or {}).get('delivery_coverage'))}")
        if did == "dir_finance":
            from agentic_core.api.operational_excellence import _load as _ops
            rows = [r for r in _ops()][-100:]
            ok = sum(1 for r in rows if r.get("success"))
            return f"recent operational rows: {len(rows)}, success rate {round(ok / len(rows), 2) if rows else 'n/a'} (virtual WST economy; real-money rails DISABLED)"
        if did == "dir_evolution":
            from agentic_core.config import data_path, load_json_tolerant
            dev = load_json_tolerant(data_path("tier_development.json"), {}) or {}
            return f"active Development Actions: {len(dev)} tier edges under continual improvement"
    except Exception as exc:
        return f"live reading unavailable ({str(exc)[:60]})"
    return "no live reading defined"


def _relevant_directors(topic: str, domain: str, k: int = 3) -> List[Dict[str, str]]:
    """Deterministic selection: score each director's mandate-word overlap with the topic+domain
    (the match reason IS the overlap — no AI guessing which specialists 'sound' relevant)."""
    import re as _re
    low = f" {topic.lower()} {domain.lower()} "
    scored = []
    for d in _BOARD:
        if d["id"] == "chief":
            continue
        words = set(_re.findall(r"[a-z]{5,}", (d["mandate"] + " " + d["title"]).lower()))
        hits = sum(1 for w in words if w in low)
        if hits:
            scored.append((hits, d["id"], d))
    scored.sort(key=lambda x: (-x[0], x[1]))
    chosen = [d for _, _, d in scored[:k]]
    if not chosen:   # no overlap → the strategy + operations directors hold the default mandate
        chosen = [d for d in _BOARD if d["id"] in ("dir_strategy", "dir_operations")]
    return chosen


@router.post("/directive")
async def board_directive(req: BoardDirective):
    """§5 (W279) — the board deliberates as SPECIALISTS: the relevant directors are selected
    deterministically, EACH contributes through its own AI call GROUNDED in live readings of the
    systems it owns, and the Chief chairs a synthesis over the directors' ACTUAL inputs — no more
    single-call invented 'Director Inputs'."""
    provenance: Dict[str, Any] = {"posture": "in-house-first", "served_by": {}, "any_external": False}
    directors = _relevant_directors(req.topic, req.domain)
    director_inputs: Dict[str, Dict[str, str]] = {}
    for d in directors:
        grounding = _director_grounding(d["id"])
        text = await _q(
            f"You are the {d['title']} on the Workstation IDBO Board.\n"
            f"Your mandate: {d['mandate']}\n"
            f"LIVE readings of the systems you own: {grounding}\n\n"
            f"Topic before the board: {req.topic}\nDomain: {req.domain}\n\n"
            "Give your specialist direction (under 80 words), grounded in the readings above — "
            "cite them where relevant.", f"board_{d['id']}", provenance)
        director_inputs[d["id"]] = {"title": d["title"], "live_grounding": grounding, "input": text}
    inputs_block = "\n\n".join(f"[{v['title']}] (live: {v['live_grounding']})\n{v['input'][:400]}"
                               for v in director_inputs.values())
    resolution = await _q(
        "You are the Chief (the Owner's digital twin), chairing the Workstation IDBO Board. "
        f"Topic: {req.topic}\nDomain: {req.domain}\n\n"
        f"The directors have ACTUALLY deliberated — their real inputs:\n{inputs_block}\n\n"
        "Synthesise and resolve (do not invent inputs beyond those above):\n"
        "## Board Position (the resolved direction)\n"
        "## Directive to the AI CEO (what to execute)\n"
        "## Guardrails (governance / arms-length constraints)", "board_directive", provenance)
    record = {
        "kind": "board_directive",
        "topic": req.topic,
        "domain": req.domain,
        "resolution": resolution,
        # §5 (W279) — the directors' REAL specialist inputs + the live groundings they drew on.
        "director_inputs": director_inputs,
        "directors_engaged": [d["id"] for d in directors],
        "ai_provenance": provenance,     # §6 — apex provenance (W270)
        "chaired_by": "Chief (Owner's Digital Twin)",
        "status": "resolved",
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    # W270 — board deliberations PERSIST (previously the resolution evaporated at response time).
    rows = _load()
    rows.append(record)
    _save(rows)
    return record
