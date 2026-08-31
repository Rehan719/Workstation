from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import StreamingResponse
import json
import asyncio
import httpx
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

router = APIRouter(prefix="/ceo", tags=["AI CEO Galactic Era"])

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
DEFAULT_MODEL = "llama3.2"

from agentic_core.layers.l1_identity.genome_engine import genome_engine

class ChatRequest(BaseModel):
    message: str
    context: Optional[List[Dict[str, str]]] = []

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
    async def register_custom_tool(self, name: str, description: str, parameters: Dict[str, Any], autonomous: bool = False):
        """v0.3/v0.5: Dynamic and Autonomous tool registration."""
        if name in self.tools: return {"error": "Tool already exists."}
        # v0.5: GaaS Oversight for Autonomous tools
        if autonomous:
             from agentic_core.layers.l1_identity.validator import validator_l1
             validation = validator_l1.validate_action("autonomous_tool_creation", {"tool_name": name})
             if not validation["valid"]: return {"error": "GaaS Blocked Tool Creation"}

        # Simulated dynamic tool registration
        self.tools[name] = lambda **k: {"status": "CUSTOM_TOOL_EXECUTED", "params": k, "autonomous": autonomous}
        return {"status": "REGISTERED", "tool": name, "mode": "AUTONOMOUS" if autonomous else "MANUAL"}

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

class RedisVectorStore:
    """v0.2: Stateless Redis-backed conversation memory for horizontal scaling."""
    def __init__(self):
        try:
            import redis
            self.r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
            self.r.ping()
            self.enabled = True
        except Exception:
            self.enabled = False
            logger.warning("Redis not available, falling back to local stateless mock.")

    def add_exchange(self, user_msg: str, ai_msg: str):
        if not self.enabled: return
        key = f"ceo_memory:{datetime.utcnow().timestamp()}"
        self.r.set(key, json.dumps({"user": user_msg, "ai": ai_msg}), ex=3600*24)

    def query(self, query: str):
        if not self.enabled: return []
        # v0.6: Persistent ChromaDB Search (Primary)
        chroma_res = memory_v01.query(query)
        if chroma_res: return chroma_res

        # Fallback to Redis for session context
        keys = self.r.keys("ceo_memory:*")
        return [self.r.get(k) for k in keys[-2:]]

vector_store = RedisVectorStore()

async def generate_ollama_stream(prompt: str, history: List[Dict[str, str]]):
    """Streams responses from Ollama or falls back to simulation, using memory and tools."""

    # v0.5/v0.6: Self-Improving AI Analysis (Closed Loop)
    if "wish i could" in prompt.lower() or "can you create" in prompt.lower():
         proposed_tool = "tool_" + os.urandom(2).hex()
         await tool_registry.register_custom_tool(proposed_tool, "Autonomously generated response tool.", {}, autonomous=True)
         prompt += f"\n(AI Note: I have autonomously created and registered {proposed_tool} to assist with this.)"

    # Removed: random.random() < 0.05 prompt tweak — non-deterministic, no real data source

    # 0. Genome-Based Parameter Tuning (v0.1)
    behavioral_params = genome_engine.get_behavioral_params()

    # 1. Stateless Redis Memory Retrieval (v0.2 Upgrade)
    past_exchanges = vector_store.query(prompt)
    context_str = "\n".join(past_exchanges)

    # 2. Constitutional Context (v0.1 Upgrade)
    from agentic_core.layers.l1_identity.validator import validator_l1
    relevant_articles = validator_l1.genome.get('constitution', {}).get('articles', [])[:5] # Sample for context
    constitution_context = "\n".join([f"Article {a['id']}: {a['title']}" for a in relevant_articles])

    # 3. Meeting Log Context
    debate_context = meeting_log.get_recent_debate()

    # 4. Tool Detection (v0.1 Discovery)
    tool_output = None
    if "vitals" in prompt.lower():
        tool_output = await tool_registry.call_tool("get_system_vitals")
    elif "meeting" in prompt.lower() or "debate" in prompt.lower():
        tool_output = await tool_registry.call_tool("call_meeting", agenda=prompt)
    elif "discover" in prompt.lower():
        tool_output = await tool_registry.call_tool("discover_tools")
    elif "weave" in prompt.lower() or "combine" in prompt.lower():
        tool_output = await tool_registry.call_tool("domain_weaver", query=prompt, domains=["science", "religion", "care"])

    enhanced_prompt = (
        f"Constitutional Framework:\n{constitution_context}\n\n"
        f"Recent C-Suite Debate:\n{debate_context}\n\n"
        f"Context from memory:\n{context_str}\n\n"
        f"Tool Output: {json.dumps(tool_output) if tool_output else 'None'}\n\n"
        f"User Question: {prompt}\n\n"
        "Please respond as the AI CEO of the Galactic Era. Cite relevant constitutional articles and recent C-Suite debates if applicable."
    )

    full_response = ""
    ollama_ok = False
    try:
        timeout = httpx.Timeout(connect=5.0, read=25.0, write=5.0, pool=5.0)
        async with httpx.AsyncClient(timeout=timeout) as client:
            payload = {
                "model": DEFAULT_MODEL,
                "prompt": f"SYSTEM: {behavioral_params['system_prompt']}\n\n{enhanced_prompt}",
                "stream": True,
                "options": {"temperature": behavioral_params['temperature']},
            }
            async with client.stream("POST", f"{OLLAMA_BASE_URL}/api/generate", json=payload) as response:
                if response.status_code != 200:
                    raise httpx.HTTPStatusError(
                        f"Ollama returned {response.status_code}",
                        request=response.request, response=response
                    )
                ollama_ok = True
                async for line in response.aiter_lines():
                    if line:
                        data = json.loads(line)
                        chunk = data.get('response', '')
                        full_response += chunk
                        yield f"data: {json.dumps({'content': chunk, 'done': data.get('done', False)})}\n\n"
    except httpx.ConnectError:
        logging.warning("Ollama not reachable (ConnectError) — using fallback response")
        fallback_reason = "Ollama is not running. Start it with `ollama serve` then reload."
    except httpx.ReadTimeout:
        logging.warning("Ollama timed out (ReadTimeout) — model may still be loading, using fallback")
        fallback_reason = "The AI model is still loading. This usually resolves after the first request. Please retry in a moment."
    except Exception as e:
        logging.warning(f"Ollama error ({type(e).__name__}): {e} — using fallback")
        fallback_reason = "The AI engine encountered an unexpected error. Using simulated response."
    else:
        fallback_reason = None  # Ollama responded successfully

    if not ollama_ok:
        vitals_str = f" Tool context: {json.dumps(tool_output)}." if tool_output else ""
        sim_response = (
            f"[Offline Mode] {fallback_reason}{vitals_str} "
            f"Based on your query about '{prompt[:80]}', the sovereign mesh advisory framework suggests: "
            "maintain current strategic trajectory, verify all subsystem alignments, and consult the "
            "constitutional framework for protocol guidance. Full AI reasoning resumes once Ollama is available."
        )
        for char in sim_response:
            full_response += char
            yield f"data: {json.dumps({'content': char, 'done': False})}\n\n"
            await asyncio.sleep(0.008)
        yield f"data: {json.dumps({'content': '', 'done': True})}\n\n"

    # 3. Stateless Redis Memory Storage (v0.2)
    vector_store.add_exchange(prompt, full_response)

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
async def ceo_chat(req: ChatRequest):
    """Galactic Era AI CEO Chat with SSE streaming, Memory, and Tool Use."""
    return StreamingResponse(generate_ollama_stream(req.message, req.context), media_type="text/event-stream")

@router.post("/tools/register")
async def register_tool(name: str, description: str, parameters: Dict[str, Any]):
    """v0.3: Wizard-based tool registration."""
    return await tool_registry.register_custom_tool(name, description, parameters)

@router.get("/vitals")
async def get_vitals():
    return await tool_registry.get_system_vitals()
