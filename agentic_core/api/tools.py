from fastapi import APIRouter, Depends
from typing import List, Dict, Any
from agentic_core.tools.discovery_engine import ToolDiscoveryEngine
from agentic_core.tools.registry import ToolRegistry

router = APIRouter(prefix="/tools", tags=["Tool Ecosystem"])
registry = ToolRegistry()
engine = ToolDiscoveryEngine(registry)

@router.get("/discover", response_model=List[Dict[str, Any]])
async def discover_tools(query: str = ""):
    """v125.0: Discover internal and external scholarly tools."""
    return engine.discover_tools(query)

@router.get("/constellation")
async def tool_constellation():
    """Tool Constellation data: tools as nodes, real registry dependencies as links.

    W400 - this used to build the map inline and raised KeyError: 'category' on a plain GET,
    because discover_tools() returns entries without a "category" key. It also appended a link
    between the first two nodes under the comment "Mock links for visualization" - an invented
    relationship presented as a real one.

    ToolDiscoveryEngine.get_constellation_map() already did this properly and was called by nobody:
    it carries real trust-derived radii, real capabilities, and links taken from the registry's
    actual dependency graph. No dependencies means no links, which is the honest answer.
    """
    return engine.get_constellation_map()
