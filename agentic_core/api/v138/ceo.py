from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import StreamingResponse
import json
import asyncio
import httpx
import os
import logging
from typing import Dict, Any, List, Optional
from pydantic import BaseModel

router = APIRouter(prefix="/ceo", tags=["AI CEO Galactic Era"])

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
DEFAULT_MODEL = "llama3.2"

class ChatRequest(BaseModel):
    message: str
    context: Optional[List[Dict[str, str]]] = []

class ToolRegistry:
    def __init__(self):
        self.tools = {
            "get_system_vitals": self.get_system_vitals,
            "deploy_agent": self.deploy_agent,
            "check_gaas_compliance": self.check_gaas_compliance
        }

    async def get_system_vitals(self):
        return {"status": "OPTIMAL", "cpu_load": "12%", "memory_usage": "4.2GB", "latency": "18ms"}

    async def deploy_agent(self, agent_type: str):
        return {"status": "DEPLOYED", "agent_id": f"agent-{agent_type}-v138", "node": "L11-ORBITAL-01"}

    async def check_gaas_compliance(self, action: str):
        return {"compliant": True, "score": 0.99, "justification": "Action aligns with Article 1127 (Autonomous Evolution)."}

    async def call_tool(self, tool_name: str, **kwargs):
        if tool_name in self.tools:
            return await self.tools[tool_name](**kwargs)
        return {"error": f"Tool {tool_name} not found."}

tool_registry = ToolRegistry()

class SimpleVectorStore:
    """Mock ChromaDB for conversation memory."""
    def __init__(self):
        self.memory = []

    def add_exchange(self, user_msg: str, ai_msg: str):
        self.memory.append({"user": user_msg, "ai": ai_msg})

    def query(self, query: str):
        # Very simple 'search'
        relevant = [m for m in self.memory if any(word in (m['user'] + m['ai']).lower() for word in query.lower().split())]
        return relevant[-2:] # Return last 2 relevant exchanges

vector_store = SimpleVectorStore()

async def generate_ollama_stream(prompt: str, history: List[Dict[str, str]]):
    """Streams responses from Ollama or falls back to simulation, using memory and tools."""

    # 1. Memory Retrieval
    past_exchanges = vector_store.query(prompt)
    context_str = "\n".join([f"User: {m['user']}\nAI: {m['ai']}" for m in past_exchanges])

    # 2. Tool Detection (Simple Keyword-based for now)
    tool_output = None
    if "vitals" in prompt.lower():
        tool_output = await tool_registry.call_tool("get_system_vitals")
    elif "deploy" in prompt.lower():
        tool_output = await tool_registry.call_tool("deploy_agent", agent_type="general")

    enhanced_prompt = f"Context from memory:\n{context_str}\n\nTool Output: {json.dumps(tool_output) if tool_output else 'None'}\n\nUser Question: {prompt}\n\nPlease respond as the AI CEO of the Galactic Era."

    full_response = ""
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            payload = {
                "model": DEFAULT_MODEL,
                "prompt": enhanced_prompt,
                "stream": True
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

    # 3. Memory Storage
    vector_store.add_exchange(prompt, full_response)

@router.post("/chat")
async def ceo_chat(req: ChatRequest):
    """Galactic Era AI CEO Chat with SSE streaming, Memory, and Tool Use."""
    return StreamingResponse(generate_ollama_stream(req.message, req.context), media_type="text/event-stream")

@router.get("/vitals")
async def get_vitals():
    return await tool_registry.get_system_vitals()
