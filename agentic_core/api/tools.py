from fastapi import APIRouter, Depends
from typing import List, Dict, Any
from agentic_core.tools.discovery_engine import ToolDiscoveryEngine

router = APIRouter(prefix="/tools", tags=["Tool Ecosystem"])
engine = ToolDiscoveryEngine()

@router.get("/discover", response_model=List[Dict[str, Any]])
async def discover_tools(query: str = ""):
    """v125.0: Discover internal and external scholarly tools."""
    if query:
        return engine.search_tools(query)
    return engine.get_all_tools()

@router.get("/constellation")
async def tool_constellation():
    """v125.0: Return data for Tool Constellation visualization."""
    tools = engine.get_all_tools()
    nodes = [{"id": t["name"], "group": t["category"]} for t in tools]
    links = []
    # Mock links for visualization
    if len(nodes) > 1:
        links.append({"source": nodes[0]["id"], "target": nodes[1]["id"], "value": 1})
    return {"nodes": nodes, "links": links}
