import logging
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)

class ToolDiscoveryEngine:
    """
    ARTICLE 641-645: v125.0 Tool Discovery Engine.
    Indexes internal reactors and external symbiotic connectors.
    """
    def __init__(self):
        self.tool_registry: Dict[str, Dict[str, Any]] = {}
        self._initialize_core_tools()

    def _initialize_core_tools(self):
        # Internal Tools
        self.register_tool("QEP_Study", "Internal", "Full Quranic Study suite with word-by-word analysis.")
        self.register_tool("Scholar_Authoring", "Internal", "Workflow engine for scholarly annotations.")
        self.register_tool("Token_Ledger", "Internal", "Cryptographic ledger for WST token management.")

        # External Tools (ARTICLE 652)
        self.register_tool("Quran.com_API", "External", "Gateway to global tafsir and recitation resources.")
        self.register_tool("JSTOR_Academic", "External", "Scholarly search for Islamic Studies papers.")

    def register_tool(self, name: str, category: str, description: str, metadata: Optional[Dict[str, Any]] = None):
        self.tool_registry[name] = {
            "name": name,
            "category": category,
            "description": description,
            "metadata": metadata or {}
        }
        logger.info(f"ToolDiscovery: Registered {category} tool: {name}")

    def search_tools(self, query: str) -> List[Dict[str, Any]]:
        query = query.lower()
        results = []
        for tool in self.tool_registry.values():
            if query in tool["name"].lower() or query in tool["description"].lower():
                results.append(tool)
        return results

    def get_all_tools(self) -> List[Dict[str, Any]]:
        return list(self.tool_registry.values())
