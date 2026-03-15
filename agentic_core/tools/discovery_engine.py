import logging
from typing import List, Dict, Any
from agentic_core.tools.registry import ToolRegistry

logger = logging.getLogger(__name__)

class ToolDiscoveryEngine:
    """
    ARTICLE D4: Tool Discovery Engine v128.0.
    Unified search and molecular trust ranking for all tools and APIs.
    """
    def __init__(self, registry: ToolRegistry):
        self.registry = registry
        # External API Index (Simulated for v128.0)
        self.external_apis = [
            {"name": "Quran.com API", "capabilities": ["text", "audio", "reciters"], "trust": 0.99},
            {"name": "JSTOR Scholarly API", "capabilities": ["academic_papers", "history"], "trust": 0.95},
            {"name": "Islamic Heritage Project", "capabilities": ["manuscripts", "archives"], "trust": 0.97},
            {"name": "Camel-Tools", "capabilities": ["arabic_morphology", "nlp"], "trust": 0.98}
        ]

    def discover_tools(self, query: str) -> List[Dict[str, Any]]:
        """
        Searches for tools based on capabilities and keywords.
        """
        logger.info(f"ToolDiscovery: Searching for tools matching: {query}")

        results = []

        # Search internal registry
        internal_tools = self.registry.list_tools()
        for tool in internal_tools:
            if query.lower() in str(tool).lower():
                tool["origin"] = "INTERNAL"
                results.append(tool)

        # Search external index
        for api in self.external_apis:
            if query.lower() in str(api).lower():
                api["origin"] = "EXTERNAL"
                results.append(api)

        # Sort by trust / molecular ranking
        return sorted(results, key=lambda x: x.get("trust", 0.9), reverse=True)

    def get_integration_guide(self, tool_name: str) -> str:
        """Returns documented integration examples for a tool."""
        return f"To integrate {tool_name}, use the SymbioticConnector framework with the provided tool_id."

    def get_constellation_map(self) -> Dict[str, Any]:
        """
        v130.1.0: Generates the Tool Constellation Map for frontend visualization.
        Tools are stars, integrations are connections.
        """
        internal = self.registry.list_tools()

        nodes = []
        links = []

        # Internal tools
        for tool in internal:
            nodes.append({
                "id": tool["name"],
                "group": "internal",
                "radius": 10 * tool.get("trust_score", 0.9),
                "capabilities": tool["capabilities"]
            })
            # Add dependency links
            deps = self.registry.dependencies.get(tool["name"], [])
            for dep in deps:
                links.append({"source": tool["name"], "target": dep, "value": 1})

        # External APIs as fixed star clusters
        for api in self.external_apis:
            nodes.append({
                "id": api["name"],
                "group": "external",
                "radius": 12,
                "capabilities": api["capabilities"]
            })

        return {
            "nodes": nodes,
            "links": links,
            "metadata": {
                "generated_at": "2024-05-23T18:00:00Z",
                "v130_convergence": "ACTIVE"
            }
        }
