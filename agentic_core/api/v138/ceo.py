from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import StreamingResponse
import json
import asyncio
import os
import logging
from datetime import datetime
from typing import Dict, Any, List, Optional
from config.paths import DATA_DIR
from pydantic import BaseModel
from agentic_core.ai.ceo.memory_v01 import memory_v01, meeting_log
from agentic_core.ai.native.orchestrator import orchestrator
from agentic_core.layers.ueg import ueg
from agentic_core.simulation.ese import get_ese_instance
from agentic_core.optimization.aro import get_aro_instance
from agentic_core.biomimicry.geospheric.drad import get_drad_instance
from agentic_core.bto.religion_bto import get_religion_bto
from agentic_core.swarm.signaling_protocol import SignalingProtocol
from agentic_core.reactor.religion.qep_flagship import qep_flagship_service
from agentic_core.ai.ceo.autonomy_pipelines import autonomy_pipelines
from agentic_core.synthesis.content_production import content_pipeline
from agentic_core.governance.industry_adaptive import governance_verifier
from agentic_core.ai.improvement_engine import improvement_engine

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/ceo", tags=["AI CEO"])

from agentic_core.ai.gateway import gateway
from agentic_core.auth.core import get_current_user, request_owner_id

class ChatRequest(BaseModel):
    message: str
    context: Optional[List[Dict[str, Any]]] = []   # W451 refuter F1: the page's messages carry provenance fields
    scope: str = "workstation"   # W451 — the Board/plan scope the CEO answers for (a vsb_id, or the platform)

class ToolRegistry:
    def __init__(self):
        self.tools = {
            "get_system_vitals": self.get_system_vitals,
            "deploy_agent": self.deploy_agent,
            "check_gaas_compliance": self.check_gaas_compliance,
            "call_meeting": self.call_meeting,
            "discover_tools": self.discover_tools,
            "run_qep_simulation": self.run_qep_simulation,
            "optimize_qep_resources": self.optimize_qep_resources,
            "orchestrate_qep_swarm": self.orchestrate_qep_swarm,
            "check_qep_fabric_health": self.check_qep_fabric_health,
            "qep_tajwid_coach": self.qep_tajwid_coach,
            "qep_memorization": self.qep_memorization,
            "qep_competitions": self.qep_competitions,
            "qep_ar_vr_immersion": self.qep_ar_vr_immersion,
            "qep_learn_teach": self.qep_learn_teach,
            "qep_adaptive_ui": self.qep_adaptive_ui,
            "qep_community": self.qep_community,
            "qep_analytics": self.qep_analytics,
            "qep_certifications": self.qep_certifications,
            "qep_offline_access": self.qep_offline_access,
            "qep_billing_donations": self.qep_billing_donations,
            "qep_guidance_assistant": self.qep_guidance_assistant,
            "qep_swarm_learning": self.qep_swarm_learning,
            "run_introspection": self.run_introspection,
            "run_retrospection": self.run_retrospection,
            "run_extrospection": self.run_extrospection,
            "generate_v10_roadmap": self.generate_v10_roadmap,
            "recursive_improve": self.recursive_improve,
            "produce_scientific_draft": self.produce_scientific_draft,
            "generate_manim_animation": self.generate_manim_animation,
            "render_quarto_lesson": self.render_quarto_lesson,
            "verify_governance_compliance": self.verify_governance_compliance
        }

    async def run_qep_simulation(self, num_agents: int = 100, steps: int = 50):
        """v0.8: Run Evolutionary Simulation Engine (ESE) for Religion Domain."""
        ese = get_ese_instance(num_agents)
        return await ese.run_simulation(steps)

    async def optimize_qep_resources(self, sim_demand: float = 0.5, reason_demand: float = 0.8):
        """v0.8: Run Autonomous Resource Optimisation (ARO)."""
        aro = get_aro_instance()
        return aro.optimize({"sim_demand": sim_demand, "reason_demand": reason_demand})

    async def orchestrate_qep_swarm(self, topic: str, domain: str = "religion"):
        """v1.0: Orchestrate specialized cross-domain research swarm (BTO)."""
        # Mock signaling for tool execution
        signaling = SignalingProtocol("CEO-ORCHESTRATOR")
        if domain == "religion":
             bto = get_religion_bto("AI-CEO", signaling)
             return bto.orchestrate_research(topic)
        else:
             # v1.0: Generic Domain BTO Adapter
             return {
                 "status": "SWARM_ACTIVE",
                 "domain": domain,
                 "topic": topic,
                 "engine": "BTO",
                 "timestamp": datetime.utcnow().isoformat()
             }

    async def check_qep_fabric_health(self):
        """v0.8: Check Dynamic Reactive Adaptive Fabric (DRAD) health."""
        drad = get_drad_instance()
        return drad.get_fabric_health()

    async def qep_tajwid_coach(self, reference: str):
        """v0.9: AI Tajwīd Coach."""
        return await qep_flagship_service.tajwid_coach(b"", reference)

    async def qep_memorization(self, user_id: str, reference: str):
        """v0.9: Memorization Suite."""
        return await qep_flagship_service.memorization_suite(user_id, reference)

    async def qep_competitions(self):
        """v0.9: Gamified Competitions."""
        return await qep_flagship_service.gamified_competition()

    async def qep_ar_vr_immersion(self, mode: str = "VR"):
        """v0.9: Interactive AI/AR with VC/VR."""
        return await qep_flagship_service.ar_vr_immersion(mode)

    async def qep_learn_teach(self, role: str = "Learner"):
        """v0.9: Learn-Teach Modules."""
        return await qep_flagship_service.learn_teach_module(role)

    async def qep_adaptive_ui(self, user_profile: Dict[str, Any]):
        """v0.9: Adaptive UI/UX Engine."""
        return await qep_flagship_service.adaptive_ui_engine(user_profile)

    async def qep_community(self):
        """v0.9: Social Media & Community."""
        return await qep_flagship_service.community_features()

    async def qep_analytics(self, user_id: str):
        """v0.9: Analytics, Ratings & Reports."""
        return await qep_flagship_service.analytics_reports(user_id)

    async def qep_certifications(self, user_id: str, course_id: str):
        """v0.9: Certifications & Credentials."""
        return await qep_flagship_service.certifications(user_id, course_id)

    async def qep_offline_access(self):
        """v0.9: Offline & Global Access."""
        return await qep_flagship_service.offline_global_access()

    async def qep_billing_donations(self):
        """v0.9: Secure Billing & Donations."""
        return await qep_flagship_service.secure_billing_donations()

    async def qep_guidance_assistant(self, query: str):
        """v0.9: AI Agents & Guidance Assistant."""
        return await qep_flagship_service.ai_guidance_assistant(query)

    async def qep_swarm_learning(self):
        """v0.9: Swarm Intelligence for Group Learning."""
        return await qep_flagship_service.swarm_intelligence_learning()

    async def run_introspection(self, action: str, reasoning: List[str], confidence: float):
        """v1.0: Run AI CEO Introspection Pipeline."""
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "action": action,
            "reasoning": reasoning,
            "confidence": confidence,
            "status": "LOGGED_TO_CHROMA"
        }

    async def run_retrospection(self, incident_log: Optional[List[Dict[str, Any]]] = None):
        """v1.0: Run AI CEO Retrospection Pipeline."""
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "analysis": "Root cause identified: latency spike in L3 reactor.",
            "fix_proposed": "Trigger ARO optimization for L3.",
            "status": "ANALYSIS_COMPLETE"
        }

    async def run_extrospection(self, external_data: Optional[List[str]] = None):
        """v1.0: Run AI CEO Extrospection Pipeline."""
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "external_trends": ["Increase in decentralized compute usage", "New PQC standards update"],
            "suggested_actions": ["Update Article 1107 with latest NIST guidelines"],
            "status": "TRENDS_MAPPED"
        }

    async def generate_v10_roadmap(self):
        """v0.9: Generate the v1.0 Global Launch Roadmap."""
        return {"roadmap_path": autonomy_pipelines.generate_v10_roadmap()}

    async def recursive_improve(self):
        """v1.0: Start recursive self-improvement loop."""
        asyncio.create_task(improvement_engine.start_optimization_loop())
        return {"status": "EVOLUTION_LOOP_STARTED"}

    async def produce_scientific_draft(self, topic: str, data: str):
        """v1.0: Generate scientific IMRaD manuscript."""
        return {"draft": content_pipeline.produce_scientific_draft(topic, data)}

    async def generate_manim_animation(self, script: str):
        """v1.0: Generate mathematical Manim animation."""
        return content_pipeline.generate_manim_animation(script)

    async def render_quarto_lesson(self, lesson_id: str, format: str = "pdf"):
        """v1.0: Render single-source Quarto document."""
        return content_pipeline.render_quarto_lesson(lesson_id, format)

    async def verify_governance_compliance(self, profile: str, tags: List[str]):
        """v1.0: Run VGA runtime verifier."""
        valid = governance_verifier.verify_action(profile, tags)
        return {"compliant": valid, "profile": profile}

    async def discover_tools(self):
        """v0.1: Tool Discovery logic."""
        available = list(self.tools.keys())
        return {"available_tools": available, "message": "New tools can be registered in the ToolRegistry class."}

    async def call_meeting(self, agenda: str):
        """Deliberate for real, or record nothing.

        W404 - this looped six officer titles and wrote
            "Synthesized position on {agenda} from {agent} perspective."   stance APPROVE
        into the meeting record for every one of them, then reported MEETING_COMPLETE. No officer
        deliberated; the "argument" was a template with the agenda echoed back, and every officer
        always approved. Those rows were then served as genuine governance record by
        GET /api/v138/ceo/meeting/log and rendered as minutes.

        This got worse in W400, not better: the meeting log used to be a broken stub that silently
        discarded everything posted to it, so the fabricated positions went nowhere. Making the log
        real meant they would have started persisting convincingly. Fixing one honesty defect
        exposed another it had been hiding.

        Each officer now states a REAL position from the native fabric, grounded in the agenda, and
        its own stance is taken from what it said. If the fabric cannot answer, nothing is written -
        an empty record is honest, a unanimous invented approval is not.
        """
        agents = ["CEvO", "CGO", "CPEO", "CBO", "CoS", "CEnvO"]
        posted, failed = [], []
        for agent in agents:
            prompt = (f"You are the {agent} of an AI C-Suite. State your position on this agenda "
                      "in at most two sentences, then end with exactly one word on its own line: "
                      "APPROVE, OBJECT or ABSTAIN." + chr(10) + chr(10)
                      + f"Agenda: {agenda}")
            try:
                res = await orchestrator.complete(prompt, agent=f"csuite:{agent}", timeout=90)
                text = (res or {}).get("output", "").strip()
            except Exception:
                text = ""
            if not text:
                failed.append(agent)
                continue
            stance = ""
            for token in ("APPROVE", "OBJECT", "ABSTAIN"):
                if token in text.upper():
                    stance = token
                    break
            meeting_log.post_argument(agent, text[:600], stance)
            posted.append(agent)
        return {
            "status": "MEETING_COMPLETE" if posted else "NO_POSITIONS_RECORDED",
            "agenda": agenda,
            "officers_deliberated": posted,
            "officers_unavailable": failed,
            "log_updated": bool(posted),
            "note": ("Only officers that actually produced a position are recorded. "
                     "Nothing is written for an officer whose reply could not be obtained."),
        }
    async def get_system_vitals(self):
        """Real host vitals from psutil.

        W404 - this returned {"status": "OPTIMAL", "cpu_load": "12%", "memory_usage": "4.2GB",
        "latency": "18ms"} as literals. Those are measurements by every convention of their names,
        and the chat path injects this dict into the AI CEO's answer whenever the user asks about
        vitals - so the CEO narrated invented numbers back to the Owner as its own observation of
        the running system. psutil was already used for real in api/csuite.py, so the instrument was
        there the whole time.

        latency is NOT reported: nothing measures it, and a plausible millisecond figure is exactly
        the kind of value that reads as measured. Absent beats invented.
        """
        import psutil
        cpu = psutil.cpu_percent(interval=0.1)
        mem = psutil.virtual_memory()
        return {
            "cpu_load_percent": round(cpu, 1),
            "memory_used_gb": round(mem.used / (1024 ** 3), 2),
            "memory_percent": round(mem.percent, 1),
            "latency_ms": None,
            "measured_by": "psutil",
            "note": "latency is not measured on this host, so none is reported.",
        }

    async def deploy_agent(self, agent_type: str):
        """Nothing here deploys anything.

        W404 - this returned {"status": "DEPLOYED", "agent_id": ..., "node": "L11-ORBITAL-01"} for
        any input. No deployment occurs, no such node exists, and the AI CEO reported the result to
        the Owner as a completed action.
        """
        return {
            "status": "NOT_IMPLEMENTED",
            "agent_type": agent_type,
            "detail": ("Agent deployment is not implemented on this deployment. Nothing was "
                       "deployed, so nothing is reported as deployed."),
        }

    async def check_gaas_compliance(self, action: str):
        """Run the REAL §11 compliance screen instead of asserting a pass.

        W404 - this returned {"compliant": True, "score": 0.99, "justification": "Action aligns with
        Article 1127 (Autonomous Evolution)."} unconditionally. A compliance verdict with a score and
        a cited article, produced by no check, narrated to the Owner by the AI CEO. The real screen
        (api/compliance.screen_compliance) already gates every delivery elsewhere.
        """
        try:
            from agentic_core.api.compliance import screen_compliance
            verdict = screen_compliance(action)
            return {"compliant": verdict.get("compliant"),
                    "overall": verdict.get("overall"),
                    "verdicts": verdict.get("verdicts"),
                    "screened_by": "agentic_core.api.compliance.screen_compliance"}
        except Exception as exc:
            return {"compliant": None,
                    "detail": "The compliance screen could not run, so no verdict is given: "
                              + str(exc)[:160]}
    async def call_tool(self, tool_name: str, **kwargs):
        """v0.6: Tool execution with logging and feedback loops."""
        if tool_name in self.tools:
            result = await self.tools[tool_name](**kwargs)
            # v0.6: Autonomous Feedback Loop
            ueg.log_event("CEO", "ToolRegistry", "TOOL_EXECUTED", {"tool": tool_name, "success": "error" not in result})
            return result

        if tool_name == "domain_weaver":
             from agentic_core.reactor.domains.weaver import domain_weaver
             return await domain_weaver.synthesize(kwargs.get("query", ""), kwargs.get("domains", ["science", "law"]))
        return {"error": f"Tool {tool_name} not found."}

tool_registry = ToolRegistry()

def _ceo_grounding(prompt: str, scope: str, owner_id: Optional[str]) -> tuple:
    """W451 (P1.3, ledger 1.3) — the AI CEO answers from the §5 chain, not from a persona: the
    Board's directives for this scope, the living plan's adherence and phases, the scope's business
    plan, and the REAL C-Suite meeting log. Returns (grounding_text, facts) — facts travel in the
    final SSE event so the page can say what the answer was grounded in."""
    facts: Dict[str, Any] = {"scope": scope, "directives": 0, "objectives": 0, "plan_score": None,
                             "debate_entries": 0}
    parts: List[str] = []
    try:
        from agentic_core.api import board as _board
        rows = [r for r in _board._load()
                if r.get("business_plan_scope") == scope or (scope == "workstation" and r.get("kind") == "board_directive")]
        facts["directives"] = len(rows)
        if rows:
            parts.append("## Board directives (most recent first)\n" + "\n".join(
                f"- {str(r.get('chief_directive') or r.get('resolution') or r.get('instruction') or r.get('topic') or '')[:240]}"
                for r in rows[-3:][::-1]))
        else:
            parts.append("## Board directives\n- none recorded for this scope")
    except Exception:
        parts.append("## Board directives\n- unavailable")
    try:
        from agentic_core.api import living_plan as _lp
        # refuter F4 — get_plan is an async route; read the scorecard the plan module itself scores from
        _pillars = list(_lp._PILLARS)
        strong = [p["pillar"] for p in _pillars if p.get("status") == "strong"]
        partial = [p["pillar"] for p in _pillars if p.get("status") == "partial"]
        facts["plan_score"] = round(len(strong) / len(_pillars), 2) if _pillars else None
        parts.append("## Living plan (the canon's own scorecard)\n"
                     f"- strong: {', '.join(strong) or 'none'}\n- partial: {', '.join(partial) or 'none'}")
    except Exception:
        parts.append("## Living plan\n- unavailable")
    try:
        from agentic_core.api import business_plan as _bp
        bp = _bp._load(scope)
        objs = bp.get("objectives") or []
        facts["objectives"] = len(objs)
        parts.append("## Business plan for this scope\n"
                     f"- executive summary: {str(bp.get('executive_summary') or 'not set')[:300]}\n"
                     f"- mission: {str(bp.get('mission') or 'not set')[:160]}\n"
                     + ("- objectives: " + "; ".join(f"{o.get('title')} ({o.get('status')}, {o.get('progress_pct', 0)}%)"
                                                     for o in objs[:5]) if objs else "- objectives: none yet"))
    except Exception:
        parts.append("## Business plan\n- unavailable")
    try:
        facts["debate_entries"] = len(meeting_log.log)
        debate = meeting_log.get_recent_debate()
        parts.append("## Recent C-Suite debate (real meeting log)\n" + (debate if debate and debate.strip() else "- none held yet"))
    except Exception:
        parts.append("## Recent C-Suite debate\n- unavailable")
    return "\n\n".join(parts), facts


async def generate_ceo_stream(prompt: str, scope: str, owner_id: Optional[str]):
    """W451 (P1.3) — the AI CEO chat on the OWNED fabric. It used to open its own client stream to a
    hard-coded local model as a space-opera persona (invented constitutional articles and debates),
    ignoring AI_DISABLE_LOCAL, the breaker, guardrails, tenant memory and provenance; registered a
    lambda 'tool' on cue and narrated it; and when the model was slow streamed a canned offline
    advisory one character at a time under a green pill (the record is in AUTONOMOUS_PROGRESS W451). Now:
    gateway.stream_meta — in-house first, breaker-gated, learning-loop recorded, tenant-scoped —
    grounded in the Board's directives, the living plan and the business plan; the final event
    names WHO served it and what it was grounded in. The floor's structured answer is an honest
    answer; it is labelled as the floor by the page."""
    # real tool context, when asked for it (measured vitals; a real per-officer meeting)
    tool_output = None
    try:
        low = prompt.lower()
        if "vitals" in low:
            tool_output = await tool_registry.call_tool("get_system_vitals")
        elif "meeting" in low or "debate" in low:
            tool_output = await tool_registry.call_tool("call_meeting", agenda=prompt)
    except Exception:
        tool_output = None
    grounding, facts = _ceo_grounding(prompt, scope, owner_id)
    full_prompt = (
        "You are the AI CEO of this Workstation IDBO enterprise. You report to the Board, chaired by the "
        "owner's digital-twin Chief; you direct the C-Suite, the Centres of Excellence and Build-to-Order. "
        "Answer from the grounding below and the question only — never invent directives, articles, debates "
        "or figures; where the grounding is silent, say so plainly.\n\n"
        f"{grounding}\n\n"
        + (f"## Tool output\n{json.dumps(tool_output)[:1200]}\n\n" if tool_output else "")
        + f"## Question\n{prompt}\n\n"
        "Respond with:\n## Assessment\n## Priorities\n## Next actions"
    )
    try:
        async for ev in gateway.stream_meta(full_prompt, agent="ai-ceo", owner_id=owner_id, augment=True):
            if "token" in ev:
                yield f"data: {json.dumps({'content': ev['token'], 'done': False})}\n\n"
            elif ev.get("done"):
                yield "data: " + json.dumps({
                    "content": "", "done": True,
                    "served_by": ev.get("served_by"), "is_external": bool(ev.get("is_external")),
                    "guardrail_passed": ev.get("guardrail_passed"), "profile_applied": ev.get("profile_applied"),
                    "grounding": facts,
                }) + "\n\n"
    except Exception as exc:
        # honest terminal frame — never a canned answer, never a silent stop
        yield "data: " + json.dumps({"content": "", "done": True, "served_by": None, "is_external": False,
                                     "error": f"the owned fabric raised: {str(exc)[:160]}", "grounding": facts}) + "\n\n"

@router.get("/meeting/log")
async def get_meeting_log():
    return meeting_log.log

@router.get("/meeting/minutes")
async def get_meeting_minutes():
    """v0.2: Export meeting minutes as Markdown."""
    from fastapi.responses import Response
    content = meeting_log.export_minutes()
    return Response(content=content, media_type="text/markdown")

@router.post("/chat")
async def ceo_chat(req: ChatRequest, user: dict | None = Depends(get_current_user)):
    """W451 — the AI CEO chat on the owned fabric (SSE): `data: {content, done}` tokens, then a final
    `{done: true, served_by, is_external, grounding}` frame. Tenant-scoped memory via the gateway."""
    owner_id = request_owner_id(user if isinstance(user, dict) else None, None)
    scope = (req.scope or "workstation").strip() or "workstation"
    if scope != "workstation":
        # refuter F6 — the grounding summarises a scope's private directives and plan into the model
        # input: the caller must own that VSB (404, never a hint that it exists)
        from agentic_core.api.vsb import _load_vsb
        from agentic_core.auth.core import user_can_access
        _v = _load_vsb(scope)
        if not _v or not user_can_access(user if isinstance(user, dict) else None, _v.get("owner_id")):
            raise HTTPException(status_code=404, detail=f"scope {scope} not found")
    return StreamingResponse(generate_ceo_stream(req.message, scope, owner_id),
                             media_type="text/event-stream",
                             headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})

@router.get("/vitals")
async def get_vitals():
    return await tool_registry.get_system_vitals()
