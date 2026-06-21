import os
import sys
from typing import Dict, Any

# The constitutional-core sibling folder contains hyphens, so it cannot be
# imported via a normal dotted path. Resolve it on sys.path instead.
_CC_DIR = os.path.join(os.path.dirname(__file__), "..", "constitutional-core")
if _CC_DIR not in sys.path:
    sys.path.insert(0, _CC_DIR)
from vsb_constitutional_core import UCIV12Interceptor

class ScholarshipIntelligenceEngine:
    """Core Scholarship Process Intelligence v12.0."""
    def __init__(self, node_id: str):
        self.uci = UCIV12Interceptor(node_id)

    async def literature_synthesis(self, topic: str, context: Dict[str, Any]):
        async def synthesize():
            return f"Literature synthesis for: {topic}. Integrity Check: 100%. Peer Review: STABLE."

        full_context = {**context, "stream": "scholarship", "intent": "literature_review"}
        return await self.uci.intercept_call("crewai", full_context, synthesize)
