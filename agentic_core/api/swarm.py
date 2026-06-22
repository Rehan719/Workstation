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

from fastapi import APIRouter
from pydantic import BaseModel

from agentic_core.ai.gateway import gateway
from agentic_core.organism.biobus import biobus

router = APIRouter(prefix="/api/v1/swarm", tags=["agent-swarm"])

_RUNS_STORE = Path("data/swarm_runs.json")


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
        routing = await gateway.query(routing_prompt, agent="ceo_router")
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
        response = await gateway.query(agent_prompt, agent=f"swarm_{aid.lower()}")
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
    synthesis = await gateway.query(synthesis_prompt, agent="ceo_synthesis")

    run = {
        "run_id": run_id,
        "task": req.task,
        "domain": req.domain,
        "realm": req.realm,
        "agents_engaged": agent_ids,
        "agent_responses": agent_responses,
        "ceo_synthesis": synthesis,
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


@router.post("/cascade")
async def cascade_orchestration(req: CascadeRequest):
    """
    Three-level cascade: CEO → C-Suite → CoE.
    Simulates the full VSB organisational intelligence hierarchy.
    """
    run_id = uuid.uuid4().hex[:10]
    start = time.time()

    biobus.fire_signal("cognitive", "swarm.cascade", f"CEO cascade: {req.mission[:80]}", 0.8)

    # In-house-first AI with provenance — the whole CEO→C-Suite→CoE cascade records which OWNED
    # resource served each tier (proves the org cascade runs on Workstation's own fabric).
    provenance: dict = {"posture": "in-house-first", "served_by": {}, "any_external": False}

    async def _q(prompt: str, agent: str) -> str:
        res = await gateway.query_meta(prompt, agent=agent)
        sb = res.get("served_by", "native")
        provenance["served_by"][sb] = provenance["served_by"].get(sb, 0) + 1
        provenance["any_external"] = provenance["any_external"] or bool(res.get("is_external"))
        return res.get("output", "")

    # Level 1: CEO sets mission
    ceo_prompt = (
        f"You are the AI CEO of a VSB. You have received this mission:\n\"{req.mission}\"\n"
        f"Domain: {req.domain}\nRealm: {req.realm}\n\n"
        "Issue a CEO Mission Directive:\n"
        "## Mission Statement (what we are achieving and why)\n"
        "## Strategic Priorities (top 3)\n"
        "## C-Suite Assignments (which executive owns which priority)\n"
        "## Success Metrics (3 measurable outcomes)\n"
        "## Timeline\n"
        "Be decisive and inspiring. This directive will cascade to your entire executive team."
    )
    ceo_directive = await _q(ceo_prompt, "cascade_ceo")

    # Level 2: C-Suite responds to directive
    csuite_roles = ["CFO", "CTO", "CMO", "COO"]
    csuite_responses: dict[str, str] = {}
    for role in csuite_roles:
        agent_info = _AGENTS[role]
        prompt = (
            f"You are the {agent_info['role']}. Your CEO has issued the following directive:\n\n"
            f"{ceo_directive[:600]}\n\n"
            f"Mission: {req.mission}\nDomain: {req.domain}\n\n"
            "Provide your functional plan (150-250 words):\n"
            "## Your Workstream\n"
            "## Key Actions (numbered, this month)\n"
            "## Resources Required\n"
            "## Metrics You Own"
        )
        csuite_responses[role] = await _q(prompt, f"cascade_{role.lower()}")

    # Level 3: CoE synthesis
    coe_specialisms = req.coe_specialisms or [req.domain, "quality", "innovation"]
    coe_responses: dict[str, str] = {}
    for specialism in coe_specialisms[:3]:
        prompt = (
            f"You are the Head of the {specialism.title()} Centre of Excellence (CoE). "
            f"The C-Suite has initiated this mission:\n\"{req.mission}\"\n\n"
            f"Provide your CoE contribution (100-150 words):\n"
            "## CoE Expertise Applied\n"
            "## Specialist Support Offered\n"
            "## Standards and Best Practice Input"
        )
        coe_responses[specialism] = await _q(prompt, f"cascade_coe_{specialism}")

    duration_ms = int((time.time() - start) * 1000)
    biobus.record_operation("swarm_cascade", "swarm.cascade", success=True, payload=f"CEO+{len(csuite_responses)} CSuite+{len(coe_responses)} CoE, {duration_ms}ms")

    return {
        "run_id": run_id,
        "mission": req.mission,
        "level_1_ceo_directive": ceo_directive,
        "level_2_csuite": csuite_responses,
        "level_3_coe": coe_responses,
        "ai_provenance": provenance,
        "duration_ms": duration_ms,
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
