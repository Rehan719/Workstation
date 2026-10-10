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
        #  W642 (FU-655, ledger v14 R5) - A LIST OF NAMES, NOT AN INDEX OF CONNECTED TOOLS. Each entry carried
        #  a typed "trust" between 0.95 and 0.99 that nothing measured, and results were ranked by it. This
        #  list connects to none of them and measures none of them. (Connector classes for two of the names
        #  exist elsewhere in the tree; whether anything uses them is not this list's to say, and it does
        #  not say.) They stay as what they are - names someone listed - and each says so.
        _LISTED = ("listed by name: this index does not connect to it or measure it; the trust figure it "
                   "used to carry was typed, not measured")
        self.external_apis = [
            {"name": "Quran.com API", "capabilities": ["text", "audio", "reciters"], "status": _LISTED},
            {"name": "JSTOR Scholarly API", "capabilities": ["academic_papers", "history"], "status": _LISTED},
            {"name": "Islamic Heritage Project", "capabilities": ["manuscripts", "archives"], "status": _LISTED},
            {"name": "Camel-Tools", "capabilities": ["arabic_morphology", "nlp"], "status": _LISTED},
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
                results.append({**tool, "origin": "INTERNAL"})

        # Search external index
        for api in self.external_apis:
            if query.lower() in str(api).lower():
                results.append({**api, "origin": "EXTERNAL"})

        #  internal (registered here) before external (listed only), then by name: an order that states
        #  nothing this platform has not measured. It used to sort by the typed trust, defaulting to 0.9.
        return sorted(results, key=lambda x: (x.get("origin") != "INTERNAL", str(x.get("name", ""))))

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
                "radius": 10,      # one size: a radius scaled by an unmeasured trust default drew a claim
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
                "generated_at": __import__("time").strftime("%Y-%m-%dT%H:%M:%SZ", __import__("time").gmtime()),
                "external_basis": "external entries are names this index lists; it connects to and measures none",
            }
        }
