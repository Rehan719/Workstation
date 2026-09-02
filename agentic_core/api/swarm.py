"""
AI Agent Swarm Orchestration — CEO delegates to specialised AI agents.

The AI CEO receives a task and autonomously delegates sub-tasks to the
appropriate C-Suite or domain agent, collects results, and synthesises
a unified response.

  POST /api/v1/swarm/delegate    — CEO delegates task to agent swarm
  POST /api/v1/swarm/cascade     — multi-level cascade (CEO → C-Suite → CoE)
  GET  /api/v1/swarm/agents      — list available agents and their capabilities
  GET  /api/v1/swarm/runs        — list recent swarm runs
"""
from __future__ import annotations

import json
import time
import uuid
from pathlib import Path
from agentic_core.config import data_path

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from agentic_core.ai.gateway import gateway
from agentic_core.organism.biobus import biobus
from agentic_core.vbs.quality import assure_delivery

router = APIRouter(prefix="/api/v1/swarm", tags=["agent-swarm"])

_RUNS_STORE = data_path("swarm_runs.json")


def _load_runs() -> list[dict]:
    _RUNS_STORE.parent.mkdir(parents=True, exist_ok=True)
    if _RUNS_STORE.exists():
        try:
            return json.loads(_RUNS_STORE.read_text())[-50:]  # keep last 50
        except Exception:
            pass
    return []


def _save_run(run: dict) -> None:
    runs = _load_runs()
    runs.append(run)
    _RUNS_STORE.write_text(json.dumps(runs[-50:], indent=2))


_AGENTS: dict[str, dict] = {
    "CEO":      {"role": "Chief Executive Officer",   "expertise": "Strategic vision, decision-making, stakeholder alignment, final synthesis"},
    "CFO":      {"role": "Chief Financial Officer",   "expertise": "Financial modelling, budgeting, funding strategy, unit economics, risk"},
    "CTO":      {"role": "Chief Technology Officer",  "expertise": "Architecture, technology selection, build vs buy, technical roadmap, AI/ML"},
    "CMO":      {"role": "Chief Marketing Officer",   "expertise": "Brand, messaging, GTM strategy, demand generation, customer acquisition"},
    "COO":      {"role": "Chief Operating Officer",   "expertise": "Process design, operational efficiency, scaling, supply chain, KPIs"},
    "CLO":      {"role": "Chief Legal Officer",       "expertise": "Contracts, compliance, IP, regulatory, employment law, risk mitigation"},
    # Full specialist C-Suite per WHOLE_VISION §5 (each officer drives its own Centre of Excellence)
    "CSO":      {"role": "Chief Strategy Officer",    "expertise": "Strategy, competitive positioning, growth options, partnerships, market entry"},
    "CPO":      {"role": "Chief Product Officer",     "expertise": "Product vision, roadmap, UX, discovery, prioritisation, lifecycle"},
    "CIO":      {"role": "Chief Information Officer",  "expertise": "Information systems, data governance, security posture, knowledge management"},
    "Forecasting": {"role": "Chief Forecasting Officer", "expertise": "Demand/financial forecasting, scenario modelling, sensitivity analysis, planning assumptions"},
    "Policy":   {"role": "Chief Policy Officer",      "expertise": "Policy, ethics, regulatory strategy, standards, public affairs, governance alignment"},
    "science":  {"role": "Chief Science Officer",     "expertise": "Research methodology, evidence synthesis, R&D strategy, academic partnerships"},
    "care":     {"role": "Chief Care Officer",        "expertise": "Healthcare pathways, patient safety, clinical governance, NICE compliance"},
    "education":{"role": "Chief Learning Officer",    "expertise": "Curriculum design, pedagogy, learning outcomes, EdTech, accreditation"},
    "law":      {"role": "Legal Domain Expert",       "expertise": "Contract law, dispute resolution, legal document generation, jurisdiction advice"},
    "religion": {"role": "Religious Affairs Advisor", "expertise": "Islamic jurisprudence, interfaith relations, halal compliance, ethics"},
}


@router.get("/agents")
async def list_agents():
    """Return all available AI agents with their capabilities."""
    return {
        "agents": [
            {"id": k, **v} for k, v in _AGENTS.items()
        ],
        "total": len(_AGENTS),
    }


@router.get("/runs")
async def list_runs():
    """Return the last 50 swarm orchestration runs."""
    runs = _load_runs()
    return {"runs": list(reversed(runs)), "total": len(runs)}


class DelegateRequest(BaseModel):
    task: str
    agent_ids: list[str] = []  # empty = CEO chooses
    context: str = ""
    realm: str = "enterprise"
    domain: str = "general"


@router.post("/delegate")
async def delegate_task(req: DelegateRequest):
    """
    CEO receives task, decides which agents to engage, collects their responses,
    and synthesises a unified executive response.
    """
    run_id = uuid.uuid4().hex[:10]
    start = time.time()

    biobus.fire_signal("cognitive", "swarm.delegate", f"CEO delegation: {req.task[:80]}", 0.7)

    # §5×§6 (W282) — /delegate joins the W268+ standard the cascade set: every call records
    # provenance + a real operational-excellence row, the synthesis is QMS-gated, and the run
    # registers its honest cognitive demand with the homeostatic controller.
    provenance: dict = {"posture": "in-house-first", "served_by": {}, "any_external": False}

    async def _dq(prompt: str, agent: str) -> str:
        _t0 = time.time()
        res = await gateway.query_meta(prompt, agent=agent)
        sb = res.get("served_by", "native")
        provenance["served_by"][sb] = provenance["served_by"].get(sb, 0) + 1
        provenance["any_external"] = provenance["any_external"] or bool(res.get("is_external"))
        try:
            from agentic_core.api.operational_excellence import record_outcome
            record_outcome("ai_call", f"agent:{agent}", served_by=sb,
                           is_external=bool(res.get("is_external")),
                           duration_ms=int((time.time() - _t0) * 1000),
                           success=bool((res.get("output") or "").strip()), ref=run_id)
        except Exception:
            pass
        return res.get("output", "")

    try:
        from agentic_core.ai.native.homeostasis import homeostasis
        homeo = homeostasis.assess(demand_nodes=2 + min(4, len(req.agent_ids or []) or 3),
                                   requested_parallel=1)
    except Exception:
        homeo = None

    # Step 1: CEO decides which agents to engage (if not specified)
    agent_ids = req.agent_ids
    if not agent_ids:
        routing_prompt = (
            f"You are the AI CEO. A task has been received:\n\"{req.task}\"\n"
            f"Domain: {req.domain}\nRealm: {req.realm}\n\n"
            f"Available agents: {', '.join(_AGENTS.keys())}\n\n"
            "Decide which 2-4 agents are best suited to address this task. "
            "Output ONLY a comma-separated list of agent IDs from the available list. No other text."
        )
        routing = await _dq(routing_prompt, "ceo_router")
        agent_ids = [a.strip().lower() for a in routing.split(",") if a.strip().lower() in _AGENTS]
        if not agent_ids:
            agent_ids = ["CFO", "CTO"]  # safe fallback

    # Step 2: Each agent processes the task
    agent_responses: dict[str, str] = {}
    for aid in agent_ids[:4]:  # max 4 agents per run
        agent_info = _AGENTS.get(aid, _AGENTS.get(aid.upper(), {"role": aid, "expertise": "general expertise"}))
        agent_prompt = (
            f"You are the {agent_info['role']} of a Virtual Sovereign Business.\n"
            f"Your expertise: {agent_info['expertise']}\n\n"
            f"Task: {req.task}\n"
            f"Domain: {req.domain}\nRealm: {req.realm}\n"
            + (f"Context: {req.context}\n" if req.context else "")
            + "\nProvide your expert analysis and recommendations from your functional perspective. "
            "Be specific, actionable, and concise (aim for 200-400 words)."
        )
        response = await _dq(agent_prompt, f"swarm_{aid.lower()}")
        agent_responses[aid] = response

    # Step 3: CEO synthesises all responses
    synthesis_input = "\n\n".join(
        f"[{aid} — {_AGENTS.get(aid, {}).get('role', aid)}]\n{resp}"
        for aid, resp in agent_responses.items()
    )
    synthesis_prompt = (
        f"You are the AI CEO. Your {len(agent_responses)} specialist agents have reported on:\n"
        f'"{req.task}"\n\n'
        f"Agent Reports:\n{synthesis_input}\n\n"
        "Synthesise these into a unified CEO executive response:\n"
        "## Executive Decision\n"
        "## Key Insights from the C-Suite\n"
        "## Recommended Course of Action (prioritised)\n"
        "## Next Steps (numbered, owner assigned to role)\n"
        "## Risks and Mitigations\n\n"
        "Be decisive. Resolve any conflicting advice between agents."
    )
    synthesis = await _dq(synthesis_prompt, "ceo_synthesis")

    # §10 (W282) — the delegate synthesis is held to the same real QMS gate as the cascade.
    try:
        _qa = await assure_delivery(synthesis, ["Executive Decision", "Recommended Course of Action",
                                                "Next Steps"], label="delegate")
        _quality = {k: _qa["quality"].get(k) for k in ("qms_gate_passed", "delivery_coverage",
                                                       "qms_non_conformance_rate", "stub_found")}
    except Exception:
        _quality = {}

    run = {
        "run_id": run_id,
        "task": req.task,
        "domain": req.domain,
        "realm": req.realm,
        "agents_engaged": agent_ids,
        "agent_responses": agent_responses,
        "ceo_synthesis": synthesis,
        # §5×§6 (W282) — delegate now proves it runs on the owned fabric like the cascade.
        "ai_provenance": provenance,
        "quality": _quality,
        "homeostasis": homeo,
        "duration_ms": int((time.time() - start) * 1000),
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    _save_run({k: v for k, v in run.items() if k != "agent_responses"})  # save compact version
    biobus.record_operation("swarm_delegate", "swarm.delegate", success=True, payload=f"{len(agent_ids)} agents, {run['duration_ms']}ms")

    return run


class CascadeRequest(BaseModel):
    mission: str
    realm: str = "enterprise"
    domain: str = "general"
    coe_specialisms: list[str] = []
    # User design control of the org structure (§5): which specialist C-Suite officers to engage — each
    # drives its own CoE. Empty = a balanced default set. Choose from the _AGENTS C-Suite keys.
    csuite_roles: list[str] = []
    # §5 (W280) — the cascade SEES the living Business Plan: `scope` selects which plan (a vsb_id or
    # 'workstation') grounds the Chief/CEO tiers; an optional `objective_id` binds the run to one
    # objective — a QMS-PASSED run writes a review back and advances planned→in_progress (never
    # auto-done — W266 semantics).
    scope: str = "workstation"
    objective_id: str | None = None


class CurateProposalRequest(BaseModel):
    item: str                       # the proposed item name to commercialise
    description: str = ""
    price_wst: float = 0.0
    vsb_id: str = ""                # attribute sales to this entity's economy (W293)
    curator: str = "owner"


@router.post("/catalogue/proposed/{run_id}/curate")
async def curate_proposed_item(run_id: str, req: CurateProposalRequest):
    """§12×§13 (W294) — a cascade-PROPOSED offering is CURATED into the live marketplace by a
    deliberate human act (the cascade proposes, the Owner/user curates — never automatic): the
    listing text is §11-screened first (a FAIL blocks publication with the verdicts — user-authored
    commercial content is exactly where the screen must have teeth), then a real marketplace
    listing is created, VSB-attributed so sales feed the entity's economy (W293). Closes the
    §5→§13→§12 loop: delivery org proposes → curation publishes → sales fund the organism."""
    from agentic_core.config import data_path as _dp, load_json_tolerant as _ljt, atomic_write_json as _awj
    store = _dp("proposed_catalogue.json")
    rows = _ljt(store, []) or []
    prop = next((p for p in rows if p.get("run_id") == run_id), None)
    if not prop:
        raise HTTPException(status_code=404, detail=f"No proposed catalogue for run {run_id}.")
    from agentic_core.api.compliance import screen_compliance
    screen = screen_compliance(f"{req.item}. {req.description}")
    if screen["overall"] == "fail":
        raise HTTPException(status_code=409, detail={
            "error": "curation_blocked_by_compliance",
            "verdicts": screen["verdicts"]})
    from agentic_core.api.marketplace import CreateListingRequest, create_listing
    listing = await create_listing(CreateListingRequest(
        name=req.item[:80], description=req.description or f"Curated from cascade {run_id}",
        author=req.curator, category="Product", price_wst=max(0.0, float(req.price_wst)),
        creator_id=req.curator, vsb_id=req.vsb_id))
    prop.setdefault("curated", []).append({
        "item": req.item, "listing_id": listing.get("id"),
        "compliance_overall": screen["overall"],
        "at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())})
    prop["status"] = "curated"
    _awj(store, rows)
    try:
        from agentic_core.gaas.v5 import UEGLogger
        UEGLogger().log({"type": "catalogue.curated", "run_id": run_id, "item": req.item[:80],
                         "listing_id": listing.get("id"), "vsb_id": req.vsb_id,
                         "compliance": screen["overall"]})
    except Exception:
        pass
    return {"run_id": run_id, "listing": listing, "compliance": screen["overall"],
            "note": "Curated by a deliberate act — the cascade proposes, never auto-publishes."}


@router.get("/catalogue/proposed")
async def proposed_catalogue(limit: int = 10):
    """§5 (W282) — the offerings the org cascade has PROPOSED (parsed + persisted per run; the
    cascade proposes, the Owner curates into the real shipped-product catalog)."""
    from agentic_core.config import data_path as _dp, load_json_tolerant as _ljt
    rows = _ljt(_dp("proposed_catalogue.json"), []) or []
    return {"proposed": list(reversed(rows[-max(1, min(int(limit), 50)):]))}


@router.get("/cascade/runs")
async def cascade_runs(limit: int = 10):
    """§5 (W268) — the persisted org-cascade run history (appraisals · Development Actions · measured
    quality · governance · provenance), newest first. The appraisal/development record survives the
    response, so the next cycle can be judged against it."""
    from agentic_core.config import data_path, load_json_tolerant
    rows = load_json_tolerant(data_path("org_cascade_runs.json"), []) or []
    return {"runs": list(reversed(rows[-max(1, min(limit, 50)):])), "total": len(rows)}


@router.post("/cascade")
async def cascade_orchestration(req: CascadeRequest):
    """
    Full VSB org cascade, apex → operational delivery, every tier run on Workstation's OWN native
    fabric with proven in-house provenance:
      Chief of the Board (founder's digital twin) → Board of Directors → AI CEO → C-Suite →
      Centres of Excellence → Business Transformation Office → Build-to-Order (operational delivery
      resources) → Products/Services catalogue.
    """
    run_id = uuid.uuid4().hex[:10]
    start = time.time()

    biobus.fire_signal("cognitive", "swarm.cascade", f"CEO cascade: {req.mission[:80]}", 0.8)

    # §8→§6 (W278): the cascade's cognitive demand is reported HONESTLY (3 apex tiers + officer+CoE
    # per selected role + optional CoEs + BTO/build/catalogue + 6 appraisals ≈ 22 calls, not 8), and
    # the homeostatic posture is BEHAVIORAL, not advisory: under granted headroom the C-Suite
    # officer+CoE pairs run CONCURRENTLY (bounded by the granted parallelism); under a protective
    # posture (granted 1) the run stays fully sequential — the organism's state genuinely shapes
    # how the organisation works. Best-effort/fail-open.
    _DEFAULT_CSUITE = ["CSO", "CFO", "CTO", "COO", "CLO"]
    _sel_probe = [r for r in (req.csuite_roles or _DEFAULT_CSUITE) if r in _AGENTS and r != "CEO"] or _DEFAULT_CSUITE
    _honest_demand = 3 + 2 * len(_sel_probe[:9]) + len((req.coe_specialisms or [])[:3]) + 3 + 6
    try:
        from agentic_core.ai.native.homeostasis import homeostasis
        homeo = homeostasis.assess(demand_nodes=_honest_demand,
                                   requested_parallel=min(4, len(_sel_probe[:9])))
    except Exception:
        homeo = None
    _granted = max(1, int((homeo or {}).get("max_parallel", 1)))
    homeostasis_adaptation = {"demand_nodes_reported": _honest_demand,
                              "granted_parallel": _granted,
                              "csuite_concurrent": _granted > 1}

    # In-house-first AI with provenance — the whole CEO→C-Suite→CoE cascade records which OWNED
    # resource served each tier (proves the org cascade runs on Workstation's own fabric).
    provenance: dict = {"posture": "in-house-first", "served_by": {}, "any_external": False}

    # §5 DEVELOP (W269) — the PREVIOUS cycle's Development Actions are APPLIED this cycle: each tier's
    # prompt carries the development action its managing tier set last run (persisted by the appraisal
    # pass below), closing the "each tier manages, appraises and DEVELOPS the tier below" loop
    # cycle-over-cycle. Development Actions previously had zero consumers.
    from agentic_core.config import atomic_write_json, data_path, load_json_tolerant
    _DEV_STORE = data_path("tier_development.json")
    _prior_dev: dict = load_json_tolerant(_DEV_STORE, {}) or {}
    development_applied: dict = {}

    # §5 (W281) — persistent tier IDENTITY: each tier accumulates a record across cascades (runs
    # served + its manager's last appraisal), so officers/CoEs/BTO are no longer re-prompted from
    # scratch — "lead and develop their specialised resources" holds OVER TIME. Deterministic
    # accumulation of real run data; no extra AI calls.
    _IDENT_STORE = data_path("tier_identity.json")
    _tier_ident: dict = load_json_tolerant(_IDENT_STORE, {}) or {}
    tier_identity_applied: dict = {}

    def _dev_for(appraisal_key: str, manager_label: str) -> str:
        rec = _prior_dev.get(appraisal_key) or {}
        action = str(rec.get("action") or "").strip()
        dev_txt = ""
        if action:
            development_applied[appraisal_key] = rec.get("run_id")
            dev_txt = (f"\n\nDEVELOPMENT ACTION from your managing tier ({manager_label}), set after the "
                       f"previous cycle's appraisal — apply it in this response:\n{action[:500]}")
        ident = _tier_ident.get(appraisal_key) or {}
        id_txt = ""
        if ident.get("runs"):
            tier_identity_applied[appraisal_key] = ident["runs"]
            id_txt = (f"\n\nYOUR TIER IDENTITY (persistent — you have served {ident['runs']} cascade "
                      f"runs; your managing tier's last appraisal of your work): "
                      f"{str(ident.get('last_appraisal', ''))[:220]}")
        return dev_txt + id_txt

    async def _q(prompt: str, agent: str) -> str:
        _qt0 = time.time()
        res = await gateway.query_meta(prompt, agent=agent)
        sb = res.get("served_by", "native")
        provenance["served_by"][sb] = provenance["served_by"].get(sb, 0) + 1
        provenance["any_external"] = provenance["any_external"] or bool(res.get("is_external"))
        # §5 (W268) — every tier call accrues a REAL operational-excellence row, so appraisals (and
        # the learning loop) judge against measured outcomes, not just same-run prose. Best-effort.
        try:
            from agentic_core.api.operational_excellence import record_outcome
            record_outcome("ai_call", f"agent:{agent}", served_by=sb,
                           is_external=bool(res.get("is_external")),
                           duration_ms=int((time.time() - _qt0) * 1000),
                           success=bool((res.get("output") or "").strip()), ref=run_id)
        except Exception:
            pass
        return res.get("output", "")

    # Tier 0a: Chief of the Board of Directors (the Owner's digital twin) — the founding mandate
    # §5 (W280) — the Chief OWNS the living Business Plan and now actually SEES it: the scoped
    # plan's REAL objectives (and the bound objective, when given) ground the apex tiers. Honest:
    # read from the plan store; an unreadable plan yields no context, never an invented one.
    _plan_ctx = ""
    try:
        from agentic_core.api.business_plan import _load as _bp_load
        _objs = (_bp_load(req.scope) or {}).get("objectives", [])
        if _objs:
            _by: dict = {}
            for _o in _objs:
                _by[_o.get("status", "?")] = _by.get(_o.get("status", "?"), 0) + 1
            _open = [o for o in _objs if o.get("status") in ("planned", "in_progress")][:5]
            _lines = "\n".join(f"- [{o.get('status')}] {o.get('title')} (KPI: {o.get('kpi', '—')})"
                               for o in _open)
            _bound = (next((o for o in _objs if o.get("id") == req.objective_id), None)
                      if req.objective_id else None)
            _plan_ctx = (f"\nTHE LIVING BUSINESS PLAN you own (scope '{req.scope}', objectives by "
                         f"status {_by}) — its open objectives:\n{_lines}\n"
                         + (f"THIS RUN DELIVERS objective {_bound.get('id')}: {_bound.get('title')} "
                            f"(KPI: {_bound.get('kpi', '—')})\n" if _bound else "")
                         + "Direct the organisation to ADVANCE this plan — cite objectives where relevant.\n")
    except Exception:
        _plan_ctx = ""

    # §5 (W281) — the cascade's Chief reasons AS the founder's lived record, not a generic twin.
    try:
        from agentic_core.api.board import founder_profile as _founder_profile
        _founder_ctx = _founder_profile()
    except Exception:
        _founder_ctx = ""
    chief_prompt = (
        f"You are the Chief of the Board of Directors — the founder's own digital twin and the apex of "
        f"this VSB's governance. A mission has been raised:\n\"{req.mission}\"\n"
        f"Domain: {req.domain}\nRealm: {req.realm}\n{_founder_ctx}{_plan_ctx}\n"
        "You own the living Business Plan and deliver it via Strategy and a living Roadmap. Set the "
        "Founding Mandate the Board and whole organisation must serve:\n"
        "## Intent & Values (why this matters; the non-negotiable principles — ethical, beneficent)\n"
        "## Strategic North Star (the outcome that defines success)\n"
        "## Strategy (how we will win — the approach the Board turns into action)\n"
        "## Living Roadmap (time-phased milestones — now / next / later, each with the outcome it lands)\n"
        "## Boundaries (what we will NOT do)\n"
        "## Mandate to the Board (what you direct the Board to govern, action-plan, and approve)\n"
        "Speak with founder-level conviction and care."
    )
    chief_mandate = await _q(chief_prompt, "cascade_chief")

    # Tier 0b: Board of Directors — governance resolution on the Chief's mandate
    board_prompt = (
        "You are the Board of Directors of this VSB. The Chief of the Board (founder's digital twin) "
        f"has issued this Founding Mandate:\n\n{chief_mandate[:600]}\n\n"
        f"Mission: {req.mission}\nDomain: {req.domain}\n\n"
        "Receive the Chief's strategy and deliver it through Action Planning with timelines, resourced "
        "tasks and project management, then delegate to the AI CEO:\n"
        "## Resolution (approve / approve-with-conditions, with reasons)\n"
        "## Governance Guardrails (risk, compliance, ethics the executive must honour)\n"
        "## Action Plan (the resolution turned into delivery: numbered tasks, each with an owner-role, a "
        "timeline, and the resource it needs — i.e. real project management)\n"
        "## Authority Delegated to the AI CEO (scope + accountabilities)\n"
        "## Board-level Success Criteria"
    )
    board_resolution = await _q(board_prompt + _dev_for("chief_appraises_board", "Chief of the Board"), "cascade_board")

    # Tier 1: AI CEO — executes under the Board's resolution
    ceo_prompt = (
        f"You are the AI CEO of a VSB, accountable to the Board. The Board has resolved:\n\n"
        f"{board_resolution[:600]}\n\n"
        f"Mission:\n\"{req.mission}\"\nDomain: {req.domain}\nRealm: {req.realm}\n{_plan_ctx}\n"
        "Issue a CEO Mission Directive that honours the Board's guardrails:\n"
        "## Mission Statement (what we are achieving and why)\n"
        "## Strategic Priorities (top 3)\n"
        "## C-Suite Assignments (which executive owns which priority)\n"
        "## Success Metrics (3 measurable outcomes)\n"
        "## Timeline\n"
        "Be decisive and inspiring. This directive will cascade to your entire executive team."
    )
    ceo_directive = await _q(ceo_prompt + _dev_for("board_appraises_ceo", "Board of Directors"), "cascade_ceo")

    # Level 2: the specialist C-Suite (§5) — user-reconfigurable (req.csuite_roles); each officer leads
    # AND develops its own Centre of Excellence (the §5 "each drives their CoE" linkage). Empty selection
    # → a balanced default set; only known C-Suite roles are engaged (CEO is the apex, not in the set).
    _CSUITE_POOL = ["CSO", "CFO", "CTO", "CPO", "COO", "CIO", "CLO", "Forecasting", "Policy"]
    selected = _sel_probe[:9]
    csuite_responses: dict[str, str] = {}
    coe_responses: dict[str, str] = {}

    async def _run_officer(role: str) -> tuple:
        agent_info = _AGENTS[role]
        prompt = (
            f"You are the {agent_info['role']}. Your CEO has issued the following directive:\n\n"
            f"{ceo_directive[:600]}\n\n"
            f"Mission: {req.mission}\nDomain: {req.domain}\n\n"
            "Provide your functional plan (150-250 words):\n"
            "## Your Workstream\n"
            "## Key Actions (numbered, this month)\n"
            "## Resources Required\n"
            "## Metrics You Own\n"
            "## Your Centre of Excellence (the specialist team/capability you stand up and develop)"
        )
        cs = await _q(prompt + _dev_for("ceo_appraises_csuite", "AI CEO"), f"cascade_{role.lower()}")
        # That officer DRIVES its CoE — specialist functional + operational delivery for its workstream.
        coe_prompt = (
            f"You are the Head of the Centre of Excellence reporting to the {agent_info['role']} "
            f"({agent_info['expertise']}). Your officer's plan:\n{cs[:400]}\n\n"
            f"Mission: {req.mission}\nDomain: {req.domain}\n\n"
            "Deliver your CoE contribution (100-150 words):\n"
            "## Specialist Capability Applied\n## Operational Delivery (what your team produces)\n"
            "## Standards & Best Practice Enforced"
        )
        coe = await _q(coe_prompt + _dev_for("csuite_appraises_coe", "your C-Suite officer"), f"cascade_coe_{role.lower()}")
        return role, cs, coe

    if _granted > 1:
        # §8 headroom granted → the officer+CoE pairs run CONCURRENTLY, bounded by the grant.
        import asyncio as _aio
        _sem = _aio.Semaphore(_granted)

        async def _bounded(role: str) -> tuple:
            async with _sem:
                return await _run_officer(role)
        for role, cs, coe in await _aio.gather(*[_bounded(r) for r in selected]):
            csuite_responses[role] = cs
            coe_responses[f"{role} CoE"] = coe
    else:
        # protective posture → fully sequential (the organism's state shapes the org's tempo)
        for role in selected:
            _r, cs, coe = await _run_officer(role)
            csuite_responses[role] = cs
            coe_responses[f"{role} CoE"] = coe
    # Optional additional domain CoEs the user explicitly requested (beyond the per-officer CoEs).
    for specialism in (req.coe_specialisms or [])[:3]:
        prompt = (
            f"You are the Head of the {specialism.title()} Centre of Excellence (CoE). "
            f"The C-Suite has initiated this mission:\n\"{req.mission}\"\n\n"
            "Provide your CoE contribution (100-150 words):\n"
            "## CoE Expertise Applied\n## Specialist Support Offered\n## Standards and Best Practice Input"
        )
        coe_responses[specialism] = await _q(prompt, f"cascade_coe_{specialism}")

    # Tier 4: Business Transformation Office — turns strategy + CoE input into a transformation programme
    bto_prompt = (
        "You are the Business Transformation Office (BTO) of this VSB. The CEO directive and the Centres "
        f"of Excellence have shaped the approach for this mission:\n\"{req.mission}\"\n\n"
        f"CEO directive (extract):\n{ceo_directive[:400]}\n\n"
        "Define the Transformation Programme that converts strategy into delivery:\n"
        "## Workstreams (the transformation initiatives, sequenced)\n"
        "## Operating Model Changes (capabilities, processes, roles to stand up)\n"
        "## Delivery Roadmap (phases with milestones)\n"
        "## Dependencies & Risks\n"
        "## Handover to Build-to-Order (what the delivery engine must produce)"
    )
    bto_programme = await _q(bto_prompt + _dev_for("ceo_appraises_bto", "AI CEO"), "cascade_bto")

    # ── §5×§7 (W272) — the BTO REQUISITIONS the Resource Fabric for real: the deterministic W263
    # word-overlap matcher (no AI, no guessing — the match reason IS the overlap) over the mission +
    # the BTO's own programme selects up to TWO light, bounded, side-effect-free facilities, and their
    # REAL handlers RUN as part of this cascade. Build-to-Order then assembles from GENUINE facility
    # outputs, not prose about facilities. Fail-soft: a facility error never breaks the cascade.
    fabric_requisitions: list = []
    try:
        import re as _re2
        from agentic_core.api.resource_fabric import _BY_ID as _FABRIC_BY_ID, _run_real_resource
        from agentic_core.ai.native.orchestrator import NativeOrchestrator as _NO
        _low = f" {req.mission.lower()} {bto_programme.lower()[:2000]} "
        _scored = []
        for _rid in _NO._TREE_FABRIC_ALLOWED:
            _r = _FABRIC_BY_ID.get(_rid)
            if not _r:
                continue
            _words: set = set()
            for _cap in (_r.get("capabilities") or []):
                _words.update(_re2.findall(r"[a-z]{5,}", str(_cap).lower()))
            _words.update(_re2.findall(r"[a-z]{5,}", str(_r.get("name", "")).lower()))
            _hits = sum(1 for _w in _words if _w in _low)
            if _hits >= 2:
                _scored.append((_hits, _rid))
        for _hits, _rid in sorted(_scored, reverse=True)[:2]:
            try:
                _fr = await _run_real_resource(_rid, {}, req.mission, req.domain)
                if _fr and not _fr.get("error"):
                    fabric_requisitions.append({
                        "resource": _rid, "ran": _fr.get("ran"), "match_hits": _hits,
                        "output": str(_fr.get("output", ""))[:400],
                    })
            except Exception:
                pass
    except Exception:
        pass
    _fabric_ctx = ""
    if fabric_requisitions:
        _fabric_ctx = (
            "\nREAL facility outputs — you requisitioned these Resource-Fabric facilities and they RAN "
            "for this mission; assemble your plan FROM these genuine results (cite them):\n" +
            "\n".join(f"- [fabric:{f['resource']} · ran {f['ran']}] {f['output'][:280]}"
                      for f in fabric_requisitions) + "\n")

    # Tier 5: Build-to-Order — operational delivery: assemble delivery resources + a work breakdown
    build_prompt = (
        "You are the Build-to-Order (BTO) operational delivery engine of this VSB. You receive this "
        f"transformation programme:\n\n{bto_programme[:500]}\n\n"
        f"Mission: {req.mission}\nDomain: {req.domain}\n{_fabric_ctx}\n"
        "Produce the Operational Delivery Plan:\n"
        "## Operational Delivery Resources (the engines/reactors/factories/labs/teams + digital "
        "resources to assemble from the Resource Fabric, and how they combine)\n"
        "## Work Breakdown (build order, owners, sequence)\n"
        "## Quality Gates & Acceptance Criteria\n"
        "## Go-Live & Operations (how it runs once delivered)"
    )
    build_to_order = await _q(build_prompt + _dev_for("bto_appraises_build", "Business Transformation Office"), "cascade_build_to_order")

    # Products / Services catalogue — what Build-to-Order will actually deliver to customers
    catalogue_prompt = (
        "You are the Build-to-Order delivery engine compiling the customer-facing Products & Services "
        f"Catalogue for this venture.\nMission: {req.mission}\nDomain: {req.domain}\n\n"
        "List 4-8 concrete products/services this VSB will deliver. For EACH item give:\n"
        "- Name\n- One-line description (the value to the customer)\n- Type (product | service)\n"
        "- Primary delivery resource(s) that produce it\n"
        "Be specific and realistic to the mission and domain; do not invent metrics or guarantees."
    )
    products_services_catalogue = await _q(catalogue_prompt, "cascade_catalogue")

    # §5 (W282) — the Products/Services catalogue LANDS instead of terminating in prose: item names
    # are parsed deterministically and persisted as PROPOSED offerings (`proposed_catalogue.json`,
    # queryable at GET /swarm/catalogue/proposed). The cascade PROPOSES — publishing into the real
    # shipped-product catalog stays a deliberate curation decision, never automatic. Honest:
    # unparseable output persists as raw text with zero items.
    catalogue_items: list = []
    try:
        import re as _re4
        for _m in _re4.finditer(r"(?:^|\n)\s*(?:[-*•]|\d+[.)])\s*(?:\*\*)?\s*(?:Name:?\s*)?"
                                r"([A-Z][^\n|*:]{2,70})", products_services_catalogue):
            _nm = _m.group(1).strip().rstrip(":").strip()
            if _nm and not _nm.lower().startswith(("one-line", "type (", "primary", "be specific", "list ")):
                catalogue_items.append(_nm)
        catalogue_items = list(dict.fromkeys(catalogue_items))[:8]
        _cat_store = data_path("proposed_catalogue.json")
        _cat = load_json_tolerant(_cat_store, []) or []
        _cat.append({"run_id": run_id, "mission": req.mission[:160], "domain": req.domain,
                     "status": "proposed", "items": catalogue_items,
                     "raw": products_services_catalogue[:2000],
                     "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())})
        atomic_write_json(_cat_store, _cat[-50:])
    except Exception:
        pass

    # ── §10 Solution-Quality Bar + the living QMS gate — run BEFORE the appraisal pass (W268) so the
    # appraising tiers judge against this run's REAL measured outcomes, not just same-run prose.
    _qa = await assure_delivery(
        f"{build_to_order}\n{products_services_catalogue}",
        ["Operational Delivery Resources", "Work Breakdown", "Quality Gates", "Go-Live"],
        label="cascade")
    quality: dict = _qa["quality"]
    biomimetic: dict = _qa["biomimetic"]

    # §5 (W268) — the MEASURED outcomes block every appraisal is grounded in: the real QMS gate,
    # coverage, the stateful non-conformance rate, provenance, and the tiers' accrued operational
    # stats. Nothing here is generated — every figure is read from the systems that measured it.
    try:
        from agentic_core.api.operational_excellence import _load as _ops_load
        _ops_rows = [r for r in _ops_load() if str(r.get("resource", "")).startswith("agent:cascade_")][-50:]
        _ops_ok = sum(1 for r in _ops_rows if r.get("success"))
        _ops_stats = {"recent_tier_calls": len(_ops_rows),
                      "success_rate": round(_ops_ok / len(_ops_rows), 3) if _ops_rows else None}
    except Exception:
        _ops_stats = {}
    try:
        from agentic_core.api.resource_fabric import _BY_ID as _FB
        _fabric_catalogue_n = len(_FB)
    except Exception:
        _fabric_catalogue_n = 0
    # §5×§6 (W275) — measured QUALITY feeds the learning loop: the run's REAL QMS verdict is
    # recorded against the model(s) that served this cascade most, so routing positively selects
    # models whose work passes the gate — not merely models that return non-empty text.
    # (W433 corrected "the model that predominantly served" — on a tie, none did.)
    try:
        from agentic_core.api.operational_excellence import record_outcome as _rq
        if provenance.get("served_by"):
            # §4.5 class (W433) — this was `max(..., key=count)[0]`, which returns the FIRST maximal
            # entry in dict order. On a tie ({ollama: 3, native: 3}) one model was arbitrarily
            # credited or blamed for the WHOLE cascade's QMS verdict — and unlike the other sites in
            # this class, that is not merely displayed: the outcome feeds model_health(), whose
            # success_rate `orchestrator._reorder_by_health()` uses to ORDER model selection and to
            # deprioritise a model below the native floor. An arbitrary attribution moved routing.
            #
            # When several models served equally, none PREDOMINATED — the comment above claimed one
            # did. The verdict is theirs jointly, so it is recorded against each of them rather than
            # against whichever the dict happened to list first. With a clear leader this reduces to
            # exactly the previous behaviour.
            _counts = provenance["served_by"]
            _top_n = max(_counts.values())
            _top_models = sorted(m for m, n in _counts.items() if n == _top_n)
            for _m in _top_models:
                _rq("model_quality", "cascade_qms_verdict", served_by=_m,
                    is_external=bool(provenance.get("any_external")),
                    success=bool(quality.get("qms_gate_passed")), ref=run_id)
    except Exception:
        pass
    measured_block = (
        "Measured outcomes for THIS run (judge against these — do not merely restate the text):\n"
        f"- QMS gate passed: {quality.get('qms_gate_passed')}\n"
        f"- Delivery coverage: {quality.get('delivery_coverage')}\n"
        f"- QMS non-conformance rate (stateful, all-time): {quality.get('qms_non_conformance_rate')}\n"
        f"- Stub/placeholder content detected: {quality.get('stub_found')}\n"
        f"- Served in-house: {not provenance['any_external']} (by: {provenance['served_by']})\n"
        + (f"- Recent cascade-tier call success rate: {_ops_stats.get('success_rate')} "
           f"over {_ops_stats.get('recent_tier_calls')} calls\n" if _ops_stats.get("recent_tier_calls") else "")
        # §5×§7 (W272) — the managing tiers see the LIVE fabric, not prose about it: what the BTO
        # actually requisitioned and ran this run, against the real catalogue size.
        + (f"- Fabric facilities requisitioned AND run this cascade: "
           f"{[f['resource'] for f in fabric_requisitions]}\n" if fabric_requisitions else
           "- Fabric facilities requisitioned this cascade: none matched\n")
        + (f"- Resource-Fabric catalogue size: {_fabric_catalogue_n}\n" if _fabric_catalogue_n else "")
    )

    # ── §5: each tier MANAGES, APPRAISES and DEVELOPS the tier below (arms-length). After the top-down
    # delegation, a bounded upward appraisal pass — each managing tier appraises the tier below's output
    # GROUNDED IN THE MEASURED OUTCOMES ABOVE and sets a development action (continual improvement),
    # without lower tiers instructing higher ones.
    appraisals: dict = {}
    for key, manager, below_label, below_text in (
        ("chief_appraises_board", "Chief of the Board", "the Board's action plan", board_resolution),
        ("board_appraises_ceo", "Board of Directors", "the AI CEO's directive", ceo_directive),
        ("ceo_appraises_csuite", "AI CEO", "the C-Suite's functional plans",
         "\n".join(f"- {r}: {t[:160]}" for r, t in csuite_responses.items())),
        # W269 — the two previously-missing edges: every produced tier now has an appraising manager
        ("csuite_appraises_coe", "specialist C-Suite (each officer, for the CoE it drives)",
         "the Centres of Excellence's contributions",
         "\n".join(f"- {r}: {t[:160]}" for r, t in coe_responses.items())),
        ("ceo_appraises_bto", "AI CEO", "the Business Transformation Office's transformation programme",
         bto_programme),
        ("bto_appraises_build", "Business Transformation Office", "Build-to-Order's delivery plan", build_to_order),
    ):
        appraisals[key] = await _q(
            f"You are the {manager}. Arms-length, you MANAGE, APPRAISE and DEVELOP the tier directly below "
            f"you.\n\n{measured_block}\nAppraise {below_label}:\n\n{str(below_text)[:600]}\n\n"
            "## Appraisal (strengths · gaps · risks — cite the measured outcomes where relevant)\n"
            "## Development Action (how you will develop and improve that tier next cycle)\n"
            "Be specific and constructive.", f"appraise_{key}")

    # §5 DEVELOP (W269) — persist each appraisal's Development Action so the NEXT cycle applies it
    # (the injection at the top of this function). Extraction is honest: the '## Development Action'
    # section when present, else the full appraisal text (bounded) — never fabricated.
    try:
        import re as _re
        for _k, _text in appraisals.items():
            _parts = _re.split(r"##\s*Development Action[^\n]*\n?", str(_text), maxsplit=1, flags=_re.I)
            _action = (_parts[1] if len(_parts) > 1 else str(_text)).strip()[:600]
            if _action:
                _prior_dev[_k] = {"action": _action, "run_id": run_id,
                                  "at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
            # §5 (W281) — accumulate the tier's persistent identity from this run's REAL appraisal
            _prev_id = _tier_ident.get(_k) or {}
            _tier_ident[_k] = {"runs": int(_prev_id.get("runs", 0)) + 1,
                               "last_appraisal": str(_text)[:300],
                               "last_run_id": run_id,
                               "updated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
        atomic_write_json(_DEV_STORE, _prior_dev)
        atomic_write_json(_IDENT_STORE, _tier_ident)
    except Exception:
        pass

    # ── §5: the AI CEO INTEGRATES the living management systems — ALL FOUR now COMPUTE over this
    # run (W270): DCMS commits real SHA3-512 versioned artifacts; QMS ran the real stateful gate
    # (above, before the appraisals); BMS computes unit economics and EMS carbon over the run's OWN
    # measured telemetry (tier artifacts produced × a duration-derived energy ESTIMATE — the $/Wh and
    # kgCO2/Wh rates are the registry catalogue's declared simulated constants, honestly labelled).
    management_systems: dict = {"integrated": [], "document_control": {}, "catalogue": []}
    try:
        from agentic_core.vbs.registry import dcms, CATALOGUE as _VBS_CAT
        management_systems["catalogue"] = _VBS_CAT
        management_systems["integrated"] = [s["id"] for s in _VBS_CAT]
        for aid, content in (
            ("ceo_directive", {"tier": "AI CEO", "text": ceo_directive[:4000]}),
            ("board_action_plan", {"tier": "Board of Directors", "text": board_resolution[:4000]}),
            ("bto_programme", {"tier": "Business Transformation Office", "text": bto_programme[:4000]}),
            ("build_to_order", {"tier": "Build-to-Order", "text": build_to_order[:4000]}),
        ):
            management_systems["document_control"][aid] = await dcms.commit_artifact(f"{run_id}:{aid}", content, "AI CEO")
    except Exception as exc:
        management_systems["error"] = str(exc)
    try:
        from agentic_core.vbs.registry import bms, ems
        _insights = len(management_systems.get("document_control", {})) + len(appraisals)
        _energy_wh = round(max(0.1, (time.time() - start) / 60.0), 3)   # duration-derived ESTIMATE
        _unit = await bms.calculate_unit_economics(_insights, _energy_wh)
        management_systems["bms"] = {
            "cost_per_insight_usd": round(float(_unit.get("cost_per_insight", 0.0)), 6),
            "roi": round(float(_unit.get("roi", 0.0)), 3), "status": _unit.get("status"),
            "insights_count": _insights, "energy_wh_estimate": _energy_wh,
            "caveat": "energy is a duration-derived estimate; $/Wh is the catalogue's simulated constant",
        }
        _eff = await ems.monitor_efficiency(_energy_wh)
        management_systems["ems"] = {
            "efficiency_gain": float(_eff), "total_co2_kg": round(float(ems.total_co2_kg), 6),
            "energy_wh_estimate": _energy_wh,
            "caveat": "kgCO2/Wh + efficiency are the catalogue's simulated constants over measured duration",
        }
    except Exception:
        pass

    # ── §5: Change Control — arms-length constitutional governance over the WHOLE delivery (gaas.v5).
    governance: dict = {"status": "ungoverned", "arms_length": True}
    try:
        from agentic_core.gaas.v5 import UnifiedConstitutionalInterceptorV16Omega, UEGLogger
        _gov_engine = UnifiedConstitutionalInterceptorV16Omega("org-cascade-node", UEGLogger())

        async def _attest() -> str:
            return "Org cascade (Chief → Build-to-Order) attested under v16-Omega constitutional supervision."
        _gov = await _gov_engine.intercept({"intent": "org_cascade", "domain": req.domain}, _attest)
        governance = {"status": _gov.status, "checkpoint": _gov.checkpoint_id, "node": _gov.node, "arms_length": True}
    except Exception as exc:
        governance = {"status": "ungoverned", "arms_length": True, "error": str(exc)}

    # ── §6: seal the full org delivery into the UEG hash-chained provenance ledger (verifiable in-house).
    ueg_hash = None
    try:
        from agentic_core.ueg.registry import ueg_ledger
        ueg_hash = await ueg_ledger.log_event("org_cascade", {
            "run_id": run_id, "mission": req.mission[:200], "domain": req.domain,
            "tiers": ["chief", "board", "ceo", "csuite", "coe", "bto", "build_to_order"],
            "served_by": provenance["served_by"], "any_external": provenance["any_external"],
            "governance": governance.get("status"),
            "document_control": list(management_systems.get("document_control", {}).keys()),
            "appraisals": list(appraisals.keys()),
            "qms_gate_passed": quality.get("qms_gate_passed"),
            "delivery_coverage": quality.get("delivery_coverage"),
            "compliance_overall": (quality.get("compliance") or {}).get("overall"),   # §11 (W287)
            "fabric_requisitioned": [f["resource"] for f in fabric_requisitions],
        }, actor="AI CEO")
    except Exception:
        pass

    duration_ms = int((time.time() - start) * 1000)
    biobus.record_operation("swarm_cascade", "swarm.cascade", success=True, payload=f"Chief+Board+CEO+{len(csuite_responses)} CSuite+{len(coe_responses)} CoE+BTO+BuildToOrder, {duration_ms}ms")

    # §5 (W280) — a cascade bound to a plan objective DELIVERS it: on a QMS-passed run a review
    # writes back onto the objective (with the run id + what the BTO requisitioned) and
    # planned→in_progress advances; a failed gate NEVER advances (W266 semantics — never auto-done).
    plan_binding = None
    if req.objective_id:
        plan_binding = {"objective_id": req.objective_id, "scope": req.scope, "advanced": False}
        try:
            from agentic_core.api.business_plan import _load as _bp_load2, _save as _bp_save2
            _fresh = _bp_load2(req.scope)
            _tgt = next((o for o in _fresh.get("objectives", []) if o.get("id") == req.objective_id), None)
            if _tgt is None:
                plan_binding["result"] = "objective_not_found"
            elif not quality.get("qms_gate_passed"):
                plan_binding["result"] = "qms_failed_no_advance"
            else:
                _tgt.setdefault("reviews", []).append({
                    "at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                    "status": "in_progress" if _tgt.get("status") == "planned" else _tgt.get("status"),
                    "note": f"§5 org cascade {run_id} delivered against this objective — QMS gate passed.",
                    "org_cascade_run": {"run_id": run_id,
                                        "fabric_requisitions": [f["resource"] for f in fabric_requisitions]},
                })
                if _tgt.get("status") == "planned":
                    _tgt["status"] = "in_progress"
                _bp_save2(_fresh)
                plan_binding.update({"advanced": True, "result": "review_written",
                                     "status": _tgt.get("status")})
        except Exception as exc:
            plan_binding["result"] = f"error: {exc}"[:120]

    # §12×§5 (W293) — a QMS-PASSED, VSB-scoped delivery EARNS: the declared simulated tariff is
    # recorded as the entity's revenue (consumed by its next autonomous cycle), and the W271 BMS
    # estimate is recorded as the run's cost side — the delivery org's real work now funds the
    # economic organism (virtual WST; honest simulation constants, never real money). Best-effort.
    economic_event = None
    if req.scope != "workstation" and quality.get("qms_gate_passed"):
        try:
            from agentic_core.economy.revenue import SIM_DELIVERY_TARIFF_WST, record_event
            _rev = record_event(req.scope, "revenue", SIM_DELIVERY_TARIFF_WST, "cascade_delivery",
                                ref=run_id, note="QMS-passed org-cascade delivery (simulated tariff)")
            _bms = (management_systems.get("bms") or {})
            _cost = round(float(_bms.get("cost_per_insight_usd") or 0.0)
                          * int(_bms.get("insights_count") or 0), 6)
            if _cost > 0:
                record_event(req.scope, "cost", _cost, "cascade_delivery_cost", ref=run_id,
                             note="BMS unit-economics estimate for this run (simulated constants)")
            economic_event = {"revenue_wst": _rev["amount_wst"], "cost_wst": _cost,
                              "basis": "simulated tariff + BMS estimate — virtual WST only"}
        except Exception:
            pass

    # §5 (W268) — PERSIST the cascade run (previously only /delegate persisted; cascade runs — with
    # their appraisals and Development Actions — evaporated at response time). Compact + capped + atomic;
    # a non-colliding store (swarm_cascades.json holds fabric cascade DEFINITIONS, not runs).
    try:
        from agentic_core.config import atomic_write_json, data_path, load_json_tolerant
        _runs_store = data_path("org_cascade_runs.json")
        _runs = load_json_tolerant(_runs_store, []) or []
        _runs.append({
            "run_id": run_id, "mission": req.mission[:200], "domain": req.domain,
            "csuite_engaged": selected, "appraisals": appraisals,
            "quality": {**{k: quality.get(k) for k in ("qms_gate_passed", "delivery_coverage",
                                                       "qms_non_conformance_rate", "stub_found")},
                        # §11 (W287) — the persisted run record carries the compliance verdict
                        "compliance_overall": (quality.get("compliance") or {}).get("overall")},
            "governance": governance.get("status"), "ueg_hash": ueg_hash,
            "served_by": provenance["served_by"], "any_external": provenance["any_external"],
            "fabric_requisitions": [{"resource": f["resource"], "ran": f["ran"],
                                     "match_hits": f["match_hits"]} for f in fabric_requisitions],
            "plan_binding": plan_binding, "business_plan_scope": req.scope,
            "duration_ms": duration_ms,
            "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        })
        atomic_write_json(_runs_store, _runs[-100:])
    except Exception:
        pass

    return {
        "run_id": run_id,
        "mission": req.mission,
        # §5 (W280) — which living plan grounded the apex tiers + the objective this run delivered.
        "business_plan_scope": req.scope,
        "plan_binding": plan_binding,
        # §12 (W293) — what this delivery EARNED for the entity's economy (simulated tariff; null
        # for workstation-scoped or gate-failed runs — a failed gate earns nothing).
        "economic_event": economic_event,
        # Full org hierarchy, apex → operational delivery, every tier run in-house (see ai_provenance).
        "org_hierarchy": [
            "Chief of the Board of Directors", "Board of Directors", "AI CEO", "C-Suite",
            "Centres of Excellence", "Business Transformation Office", "Build-to-Order",
        ],
        "level_0_chief_of_board": chief_mandate,
        "level_0b_board_resolution": board_resolution,
        "level_1_ceo_directive": ceo_directive,
        "level_2_csuite": csuite_responses,
        "level_3_coe": coe_responses,
        # §5 — the engaged specialist C-Suite (each drives its own CoE) + the full pool for user
        # design-control reconfiguration (pass csuite_roles to choose which officers run).
        "csuite_roster": {"engaged": selected, "available": _CSUITE_POOL, "each_drives_coe": True},
        # §5 — each tier manages, APPRAISES and DEVELOPS the tier below (arms-length upward appraisal).
        "appraisals": appraisals,
        # §5 DEVELOP (W269) — which tiers received + applied the PREVIOUS cycle's Development Action
        # (key → the run_id that set it); empty on a first run.
        "development_applied": development_applied,
        # §5 (W281) — persistent tier identity: which tiers carried their accumulated record into
        # this run (edge → runs served so far); empty on a first run.
        "tier_identity_applied": tier_identity_applied,
        # §10 Solution-Quality Bar + the living-QMS quality gate over the operational delivery.
        "quality": quality,
        # §8 — the biomimetic living-organism substrate the cascade runs within (live immune + circadian).
        "biomimetic": biomimetic,
        # §8→§6 — the homeostatic posture this heavy cascade ran under (and the ATP it expended).
        "homeostasis": homeo,
        # §8 (W278) — how the posture BEHAVIORALLY shaped this run: honest demand reported,
        # granted parallelism, and whether the C-Suite actually ran concurrently.
        "homeostasis_adaptation": homeostasis_adaptation,
        "level_4_business_transformation_office": bto_programme,
        # §5×§7 (W272) — the fabric facilities the BTO requisitioned AND ran this cascade (real
        # handler outputs, deterministic word-overlap match — empty when nothing genuinely matched).
        "fabric_requisitions": fabric_requisitions,
        "level_5_build_to_order": build_to_order,
        "products_services_catalogue": products_services_catalogue,
        # §5 (W282) — the parsed, persisted PROPOSED offerings (empty when honestly unparseable).
        "catalogue_items_proposed": catalogue_items,
        # §5: the living management systems the AI CEO integrates (with real DCMS document-control proof).
        "management_systems": management_systems,
        # §5: arms-length Change-Control / constitutional governance over the whole delivery.
        "governance": governance,
        # §6: verifiable hash-chained provenance for the entire org delivery (sealed into the UEG ledger).
        "ueg_hash": ueg_hash,
        "ai_provenance": provenance,
        "duration_ms": duration_ms,
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
