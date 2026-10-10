import logging
import datetime
from typing import Dict, Any, List, Optional
import uuid

logger = logging.getLogger(__name__)

class ToolRegistry:
    """
    ARTICLE 641: Central Tool Registry v130.1.0.
    Indexes all internal reactors and external scholarly APIs with versioning and dependency resolution.
    """
    def __init__(self):
        self.tools = {}
        self.dependencies = {}

    def register_tool(self, name: str, category: str, capabilities: List[str], config: Dict[str, Any], version: str = "1.0.0", deps: List[str] = None):
        """Registers a new tool or reactor into the ecosystem with v130 tracking."""
        tool_id = str(uuid.uuid4())[:8]
        self.tools[name] = {
            "id": tool_id,
            "name": name,
            "version": version,
            "category": category,
            "capabilities": capabilities,
            "config": config,
            "registered_at": datetime.datetime.now().isoformat(),
            "status": "ACTIVE",
            #  W648 (FU-678) - no trust figure: 0.95 was stamped on every tool at registration and nothing
            #  had measured it. The key is gone rather than nulled; nothing in the tree reads it from here.
        }
        if deps:
            self.dependencies[name] = deps

        logger.info(f"ToolRegistry: Registered {name} v{version} ({category})")

    def get_tool(self, name: str) -> Optional[Dict[str, Any]]:
        return self.tools.get(name)

    def list_tools(self, category: Optional[str] = None) -> List[Dict[str, Any]]:
        if category:
            return [t for n, t in self.tools.items() if t["category"] == category]
        return list(self.tools.values())
