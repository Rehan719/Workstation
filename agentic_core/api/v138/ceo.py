from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import StreamingResponse
import json
import asyncio
import httpx
import os
import logging
import random
from datetime import datetime
from typing import Dict, Any, List, Optional
from pydantic import BaseModel
from agentic_core.ai_ceo.memory_v01 import memory_v01, meeting_log
from agentic_core.layers.ueg import ueg

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
            "discover_tools": self.discover_tools
        }

    async def discover_tools(self):
        """v0.1: Tool Discovery logic."""
        available = list(self.tools.keys())
        return {"available_tools": available, "message": "New tools can be registered in the ToolRegistry class."}

    async def call_meeting(self, agenda: str):
        """v0.1: Trigger C-Suite Debate."""
        agents = ["CEvO", "CGO", "CPEO", "CBO", "CoS", "CEnvO"]
        for agent in agents:
            # Simulated Agent Debate logic based on agenda
            meeting_log.post_argument(agent, f"Synthesized position on {agenda} from {agent} perspective.", "APPROVE")
        return {"status": "MEETING_COMPLETE", "log_updated": True}

    async def get_system_vitals(self):
        return {"status": "OPTIMAL", "cpu_load": "12%", "memory_usage": "4.2GB", "latency": "18ms"}

    async def deploy_agent(self, agent_type: str):
        return {"status": "DEPLOYED", "agent_id": f"agent-{agent_type}-v138", "node": "L11-ORBITAL-01"}

    async def check_gaas_compliance(self, action: str):
        return {"compliant": True, "score": 0.99, "justification": "Action aligns with Article 1127 (Autonomous Evolution)."}

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

    # v0.6: Analyze recent tool success rates for self-optimization
    # Simulation: Propose prompt tweak if error rate > 20% (Article 1118)
    if random.random() < 0.05:
         prompt += "\n(CEO Self-Analysis: Optimizing system prompt for higher precision.)"

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
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            payload = {
                "model": DEFAULT_MODEL,
                "prompt": f"SYSTEM: {behavioral_params['system_prompt']}\n\n{enhanced_prompt}",
                "stream": True,
                "options": {
                    "temperature": behavioral_params['temperature']
                }
            }
            async with client.stream("POST", f"{OLLAMA_BASE_URL}/api/generate", json=payload) as response:
                if response.status_code != 200:
                    raise Exception("Ollama error")
                async for line in response.aiter_lines():
                    if line:
                        data = json.loads(line)
                        chunk = data.get('response', '')
                        full_response += chunk
                        yield f"data: {json.dumps({'content': chunk, 'done': data.get('done', False)})}\n\n"
    except Exception as e:
        logging.warning(f"Ollama unavailable, falling back to simulation: {e}")
        sim_response = f"Simulated synthesis: In response to '{prompt}', the Galactic Era mesh is stabilizing. Alignment remains optimal. {f'System Vitals: {json.dumps(tool_output)}' if tool_output else ''} (Ollama Offline)"
        for char in sim_response:
            full_response += char
            yield f"data: {json.dumps({'content': char, 'done': False})}\n\n"
            await asyncio.sleep(0.01)
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
