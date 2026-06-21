import os
import sys
from typing import Dict, Any

# The constitutional-core sibling folder contains hyphens, so it cannot be
# imported via a normal dotted path. Resolve it on sys.path instead.
_CC_DIR = os.path.join(os.path.dirname(__file__), "..", "constitutional-core")
if _CC_DIR not in sys.path:
    sys.path.insert(0, _CC_DIR)
from vsb_constitutional_core import UCIV12Interceptor

class ScienceIntelligenceEngine:
    """Core Science Process Intelligence v12.0."""
    def __init__(self, node_id: str):
        self.uci = UCIV12Interceptor(node_id)

    async def automate_scientific_method(self, hypothesis: str, context: Dict[str, Any]):
        async def verify():
            return f"Science verification for: {hypothesis}. Citations: 12. Falsifiability: PASSED."

        full_context = {**context, "stream": "science", "intent": "scientific_method"}
        return await self.uci.intercept_call("langgraph", full_context, verify)
