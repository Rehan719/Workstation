from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import StreamingResponse
import json
import asyncio
import httpx
import os
import logging
from typing import Dict, Any, List, Optional
from pydantic import BaseModel
from agentic_core.ai_ceo.memory_v01 import memory_v01, meeting_log

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

    async def call_tool(self, tool_name: str, **kwargs):
        if tool_name in self.tools:
            return await self.tools[tool_name](**kwargs)
        if tool_name == "domain_weaver":
             from agentic_core.reactor.domains.weaver import domain_weaver
             return await domain_weaver.synthesize(kwargs.get("query", ""), kwargs.get("domains", ["science", "law"]))
        return {"error": f"Tool {tool_name} not found."}

tool_registry = ToolRegistry()

class SimpleVectorStore:
    """Mock ChromaDB for conversation memory with persistent JSON backend."""
    def __init__(self):
        self.file_path = "agentic_core/data/memory.json"
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        self.memory = self._load_memory()

    def _load_memory(self):
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, 'r') as f:
                    data = json.load(f)
                    return data if isinstance(data, list) else []
            except:
                return []
        return []

    def _save_memory(self):
        with open(self.file_path, 'w') as f:
            json.dump(self.memory, f, indent=2)

    def add_exchange(self, user_msg: str, ai_msg: str):
        self.memory.append({"user": user_msg, "ai": ai_msg, "timestamp": str(asyncio.get_event_loop().time())})
        # Keep last 50 exchanges
        self.memory = self.memory[-50:]
        self._save_memory()

    def query(self, query: str):
        # Keyword based retrieval
        relevant = [m for m in self.memory if any(word in (m['user'] + m['ai']).lower() for word in query.lower().split())]
        return relevant[-2:] # Return last 2 relevant exchanges

vector_store = SimpleVectorStore()

async def generate_ollama_stream(prompt: str, history: List[Dict[str, str]]):
    """Streams responses from Ollama or falls back to simulation, using memory and tools."""

    # 0. Genome-Based Parameter Tuning (v0.1)
    behavioral_params = genome_engine.get_behavioral_params()

    # 1. Semantic Memory Retrieval (v0.1 Upgrade)
    past_exchanges = memory_v01.query(prompt)
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

    # 3. Semantic Memory Storage (v0.1)
    memory_v01.add_exchange(prompt, full_response)

@router.get("/meeting/log")
async def get_meeting_log():
    return meeting_log.log

@router.post("/chat")
async def ceo_chat(req: ChatRequest):
    """Galactic Era AI CEO Chat with SSE streaming, Memory, and Tool Use."""
    return StreamingResponse(generate_ollama_stream(req.message, req.context), media_type="text/event-stream")

@router.get("/vitals")
async def get_vitals():
    return await tool_registry.get_system_vitals()
